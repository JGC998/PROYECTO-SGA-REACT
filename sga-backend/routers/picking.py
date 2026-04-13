"""
Router de Picking — tablas propias del SGA (esquema sga).
Los artículos se identifican por ARTCOD (str). El stock se actual en la tabla STOCK de LIN.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from database import SessionLocal
import modelos_operacionales as op
import models
from datetime import datetime

router = APIRouter(prefix="/picking", tags=["Picking"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _generar_codigo() -> str:
    return f"PIK-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"


def _orden_to_dict(o: op.PickingOrden) -> dict:
    return {
        "id": o.id,
        "codigo": o.codigo,
        "operario_cod": o.operario_cod,
        "estado": o.estado,
        "prioridad": o.prioridad,
        "notas": o.notas,
        "creado_en": o.creado_en.isoformat() if o.creado_en else None,
        "completado_en": o.completado_en.isoformat() if o.completado_en else None,
        "lineas": [
            {
                "id": l.id,
                "articulo_cod": l.articulo_cod,
                "cantidad_solicitada": l.cantidad_solicitada,
                "cantidad_recogida": l.cantidad_recogida,
                "ubicacion_origen": l.ubicacion_origen,
                "estado": l.estado,
            }
            for l in (o.lineas or [])
        ]
    }


@router.get("/")
def listar_ordenes(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    ordenes = (
        db.query(op.PickingOrden)
        .options(joinedload(op.PickingOrden.lineas))
        .order_by(op.PickingOrden.id.desc())
        .offset(skip).limit(limit).all()
    )
    return [_orden_to_dict(o) for o in ordenes]


@router.post("/", status_code=201)
def crear_orden(item: dict, db: Session = Depends(get_db)):
    """
    Crea una orden de picking. Body esperado:
    {
      "operario_cod": "OPE01",
      "prioridad": 1,
      "notas": "...",
      "lineas": [{"articulo_cod": "ART001", "cantidad_solicitada": 5, "ubicacion_origen": "A-01"}]
    }
    """
    pik = op.PickingOrden(
        codigo=_generar_codigo(),
        operario_cod=item.get("operario_cod"),
        prioridad=item.get("prioridad", 1),
        notas=item.get("notas"),
        estado="pendiente"
    )
    db.add(pik)
    db.flush()

    for l in item.get("lineas", []):
        art = db.query(models.Articulo).filter(models.Articulo.sku == l.get("articulo_cod")).first()
        if not art:
            db.rollback()
            raise HTTPException(400, f"Artículo '{l.get('articulo_cod')}' no encontrado")
        linea = op.PickingLinea(
            picking_id=pik.id,
            articulo_cod=l["articulo_cod"],
            cantidad_solicitada=l.get("cantidad_solicitada", 0),
            ubicacion_origen=l.get("ubicacion_origen"),
            estado="pendiente"
        )
        db.add(linea)

    db.commit()
    db.refresh(pik)
    return _orden_to_dict(pik)


@router.put("/{picking_id}/asignar")
def asignar_operario(picking_id: int, operario_cod: str, db: Session = Depends(get_db)):
    orden = db.query(op.PickingOrden).filter(op.PickingOrden.id == picking_id).first()
    if not orden:
        raise HTTPException(404, "Orden no encontrada")
    orden.operario_cod = operario_cod
    if orden.estado == "pendiente":
        orden.estado = "en_proceso"
    db.commit()
    return {"mensaje": "Operario asignado"}


@router.put("/{picking_id}/lineas/{linea_id}/recoger")
def marcar_linea_recogida(picking_id: int, linea_id: int, cantidad_recogida: float, db: Session = Depends(get_db)):
    linea = (
        db.query(op.PickingLinea)
        .filter(op.PickingLinea.id == linea_id, op.PickingLinea.picking_id == picking_id)
        .first()
    )
    if not linea:
        raise HTTPException(404, "Línea no encontrada")

    linea.cantidad_recogida = cantidad_recogida
    linea.estado = "completada" if cantidad_recogida >= linea.cantidad_solicitada else "parcial"
    db.commit()
    return {"mensaje": "Línea actualizada", "estado": linea.estado}


@router.put("/{picking_id}/completar")
def completar_picking(picking_id: int, db: Session = Depends(get_db)):
    """Descuenta el stock de LIN (tabla STOCK) y cierra la orden."""
    orden = (
        db.query(op.PickingOrden)
        .options(joinedload(op.PickingOrden.lineas))
        .filter(op.PickingOrden.id == picking_id)
        .first()
    )
    if not orden:
        raise HTTPException(404, "Orden no encontrada")
    if orden.estado == "completado":
        return {"mensaje": "Ya estaba completada"}

    try:
        for linea in orden.lineas:
            if linea.cantidad_recogida <= 0:
                continue

            # Buscar stock en la ubicación especificada
            q = db.query(models.Stock).filter(models.Stock.articulo_cod == linea.articulo_cod)
            if linea.ubicacion_origen:
                q = q.filter(models.Stock.ubicacion == linea.ubicacion_origen)
            stock_row = q.order_by(models.Stock.cantidad.desc()).first()

            if stock_row:
                stock_row.cantidad = (stock_row.cantidad or 0) - linea.cantidad_recogida
                if stock_row.cantidad < 0:
                    stock_row.cantidad = 0  # No permitir negativos
            linea.estado = "completada"

        orden.estado = "completado"
        orden.completado_en = datetime.utcnow()
        db.commit()
        return {"mensaje": "Picking completado y stock descontado de LIN"}
    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Error completando picking: {str(e)}")
