"""
Router de Recepciones — tablas propias del SGA (esquema sga).
Los artículos se identifican por su ARTCOD (str), no por un int.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal
import modelos_operacionales as op
import models
from datetime import datetime

router = APIRouter(prefix="/recepciones", tags=["Recepciones"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _generar_codigo() -> str:
    return f"REC-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"


def _recepcion_to_dict(r: op.Recepcion) -> dict:
    return {
        "id": r.id,
        "codigo": r.codigo,
        "proveedor_cod": r.proveedor_cod,
        "estado": r.estado,
        "fecha_esperada": r.fecha_esperada.isoformat() if r.fecha_esperada else None,
        "fecha_recepcion": r.fecha_recepcion.isoformat() if r.fecha_recepcion else None,
        "notas": r.notas,
        "creado_en": r.creado_en.isoformat() if r.creado_en else None,
        "lineas": [
            {
                "id": l.id,
                "articulo_cod": l.articulo_cod,
                "cantidad_esperada": l.cantidad_esperada,
                "cantidad_recibida": l.cantidad_recibida,
                "estado": l.estado,
                "ubicacion_destino": l.ubicacion_destino,
                "lote": l.lote,
            }
            for l in (r.lineas or [])
        ]
    }


@router.get("/")
def listar_recepciones(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    recepciones = (
        db.query(op.Recepcion)
        .options(joinedload(op.Recepcion.lineas))
        .order_by(op.Recepcion.id.desc())
        .offset(skip).limit(limit).all()
    )
    return [_recepcion_to_dict(r) for r in recepciones]


@router.post("/", status_code=201)
def crear_recepcion(item: dict, db: Session = Depends(get_db)):
    """
    Crea una recepción. Body esperado:
    {
      "proveedor_cod": "PROV01",
      "fecha_esperada": "2026-04-20T10:00:00",
      "notas": "...",
      "lineas": [{"articulo_cod": "ART001", "cantidad_esperada": 10, "ubicacion_destino": "A-01", "lote": "L001"}]
    }
    """
    rec = op.Recepcion(
        codigo=_generar_codigo(),
        proveedor_cod=item.get("proveedor_cod"),
        fecha_esperada=item.get("fecha_esperada"),
        notas=item.get("notas"),
        estado="pendiente",
    )
    db.add(rec)
    db.flush()

    for l in item.get("lineas", []):
        # Verificar que el artículo existe en LIN
        art = db.query(models.Articulo).filter(models.Articulo.sku == l.get("articulo_cod")).first()
        if not art:
            db.rollback()
            raise HTTPException(400, f"El artículo '{l.get('articulo_cod')}' no existe en la base de datos")
        linea = op.RecepcionLinea(
            recepcion_id=rec.id,
            articulo_cod=l["articulo_cod"],
            cantidad_esperada=l.get("cantidad_esperada", 0),
            cantidad_recibida=l.get("cantidad_recibida", 0),
            ubicacion_destino=l.get("ubicacion_destino"),
            lote=l.get("lote", ""),
            estado="pendiente"
        )
        db.add(linea)

    db.commit()
    db.refresh(rec)
    return _recepcion_to_dict(rec)


@router.put("/{recepcion_id}/confirmar")
def confirmar_recepcion(recepcion_id: int, db: Session = Depends(get_db)):
    """
    Confirma la recepción.
    Actualiza el STOCK de LIN incrementando las cantidades recibidas.
    """
    rec = (
        db.query(op.Recepcion)
        .options(joinedload(op.Recepcion.lineas))
        .filter(op.Recepcion.id == recepcion_id)
        .first()
    )
    if not rec:
        raise HTTPException(404, "Recepción no encontrada")
    if rec.estado == "completada":
        raise HTTPException(400, "La recepción ya está completada")

    try:
        for linea in rec.lineas:
            if linea.cantidad_recibida <= 0:
                continue

            ubi = linea.ubicacion_destino or ""
            lote = linea.lote or ""

            # Buscar fila de stock existente o crear una nueva
            stock_row = (
                db.query(models.Stock)
                .filter(
                    models.Stock.articulo_cod == linea.articulo_cod,
                    models.Stock.ubicacion == ubi,
                    models.Stock.lote == lote
                )
                .first()
            )
            if stock_row:
                stock_row.cantidad = (stock_row.cantidad or 0) + linea.cantidad_recibida
            else:
                nuevo_stock = models.Stock(
                    articulo_cod=linea.articulo_cod,
                    ubicacion=ubi,
                    lote=lote,
                    cantidad=linea.cantidad_recibida,
                )
                db.add(nuevo_stock)

            # Estado de la línea
            if linea.cantidad_recibida == linea.cantidad_esperada:
                linea.estado = "recibida"
            elif linea.cantidad_recibida < linea.cantidad_esperada:
                linea.estado = "discrepancia"
            else:
                linea.estado = "recibida"

        rec.estado = "completada"
        rec.fecha_recepcion = datetime.utcnow()
        db.commit()
        return {"mensaje": "Recepción confirmada", "recepcion_id": rec.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Error confirmando recepción: {str(e)}")


@router.put("/{recepcion_id}/lineas/{linea_id}")
def actualizar_linea_recepcion(
    recepcion_id: int, linea_id: int,
    cant_recibida: float,
    ubicacion_destino: str = None,
    lote: str = None,
    db: Session = Depends(get_db)
):
    linea = (
        db.query(op.RecepcionLinea)
        .filter(op.RecepcionLinea.id == linea_id, op.RecepcionLinea.recepcion_id == recepcion_id)
        .first()
    )
    if not linea:
        raise HTTPException(404, "Línea no encontrada")

    linea.cantidad_recibida = cant_recibida
    if ubicacion_destino is not None:
        linea.ubicacion_destino = ubicacion_destino
    if lote is not None:
        linea.lote = lote

    db.commit()
    db.refresh(linea)
    return {
        "id": linea.id,
        "articulo_cod": linea.articulo_cod,
        "cantidad_esperada": linea.cantidad_esperada,
        "cantidad_recibida": linea.cantidad_recibida,
        "ubicacion_destino": linea.ubicacion_destino,
        "lote": linea.lote,
        "estado": linea.estado,
    }
