"""
Router de Inventarios — tablas propias del SGA (esquema sga).
Permite inventarios físicos que ajustan el stock de LIN (tabla STOCK).
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from database import SessionLocal
import modelos_operacionales as op
import models
from datetime import datetime

router = APIRouter(prefix="/inventarios", tags=["Inventarios"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _generar_codigo() -> str:
    return f"INV-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"


def _inv_to_dict(inv: op.Inventario) -> dict:
    return {
        "id": inv.id,
        "codigo": inv.codigo,
        "almacen_cod": inv.almacen_cod,
        "responsable_id": inv.responsable_id,
        "estado": inv.estado,
        "creado_en": inv.creado_en.isoformat() if inv.creado_en else None,
        "cerrado_en": inv.cerrado_en.isoformat() if inv.cerrado_en else None,
        "lineas": [
            {
                "id": l.id,
                "articulo_cod": l.articulo_cod,
                "ubicacion_codigo": l.ubicacion_codigo,
                "cantidad_sistema": l.cantidad_sistema,
                "cantidad_fisica": l.cantidad_fisica,
                "diferencia": l.diferencia,
            }
            for l in (inv.lineas or [])
        ]
    }


@router.get("/")
def listar_inventarios(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    inventarios = (
        db.query(op.Inventario)
        .options(joinedload(op.Inventario.lineas))
        .order_by(op.Inventario.id.desc())
        .offset(skip).limit(limit).all()
    )
    return [_inv_to_dict(i) for i in inventarios]


@router.post("/", status_code=201)
def crear_inventario(item: dict, db: Session = Depends(get_db)):
    """
    Crea un inventario físico para un almacén.
    El sistema auto-captura el stock actual de LIN como 'cantidad_sistema'.
    Body esperado: {"almacen_cod": "A1", "responsable_id": 1}
    """
    almacen_cod = item.get("almacen_cod")
    responsable_id = item.get("responsable_id", 1)

    inv = op.Inventario(
        codigo=_generar_codigo(),
        almacen_cod=almacen_cod,
        responsable_id=responsable_id,
        estado="abierto",
    )
    db.add(inv)
    db.flush()

    # Auto-generar líneas con el stock actual de LIN para ese almacén
    if almacen_cod:
        # Obtener códigos de ubicaciones del almacén
        ubicaciones = (
            db.query(models.Ubicacion)
            .filter(models.Ubicacion.almacen_cod == almacen_cod)
            .all()
        )
        codigos_ubi = {(u.codigo or "").strip(): u for u in ubicaciones}

        if codigos_ubi:
            stock_rows = (
                db.query(
                    models.Stock.articulo_cod,
                    models.Stock.ubicacion,
                    func.sum(models.Stock.cantidad).label("total")
                )
                .filter(
                    models.Stock.ubicacion.in_(list(codigos_ubi.keys())),
                    models.Stock.cantidad > 0
                )
                .group_by(models.Stock.articulo_cod, models.Stock.ubicacion)
                .all()
            )

            for art_cod, ubi_cod, cant in stock_rows:
                linea = op.InventarioLinea(
                    inventario_id=inv.id,
                    articulo_cod=art_cod.strip(),
                    ubicacion_codigo=ubi_cod.strip(),
                    cantidad_sistema=cant or 0,
                )
                db.add(linea)

    db.commit()
    db.refresh(inv)
    return _inv_to_dict(inv)


@router.put("/{inv_id}/lineas/{linea_id}")
def actualizar_linea_inventario(
    inv_id: int,
    linea_id: int,
    cantidad_fisica: float,
    db: Session = Depends(get_db)
):
    """El operario introduce lo que ha contado realmente."""
    linea = (
        db.query(op.InventarioLinea)
        .filter(op.InventarioLinea.id == linea_id, op.InventarioLinea.inventario_id == inv_id)
        .first()
    )
    if not linea:
        raise HTTPException(404, "Línea no encontrada")

    linea.cantidad_fisica = cantidad_fisica
    linea.diferencia = cantidad_fisica - linea.cantidad_sistema
    db.commit()
    db.refresh(linea)
    return {
        "id": linea.id,
        "articulo_cod": linea.articulo_cod,
        "ubicacion_codigo": linea.ubicacion_codigo,
        "cantidad_sistema": linea.cantidad_sistema,
        "cantidad_fisica": linea.cantidad_fisica,
        "diferencia": linea.diferencia,
    }


@router.post("/{inv_id}/cerrar")
def cerrar_inventario(inv_id: int, db: Session = Depends(get_db)):
    """
    Cierra el inventario y aplica los ajustes de diferencia directamente
    sobre la tabla STOCK de LIN.
    """
    inv = (
        db.query(op.Inventario)
        .options(joinedload(op.Inventario.lineas))
        .filter(op.Inventario.id == inv_id)
        .first()
    )
    if not inv:
        raise HTTPException(404, "Inventario no encontrado")
    if inv.estado == "cerrado":
        raise HTTPException(400, "El inventario ya está cerrado")

    try:
        ajustes_realizados = 0
        for linea in inv.lineas:
            if linea.cantidad_fisica is None:
                continue
            if linea.diferencia == 0:
                continue

            # Buscar la fila de stock correspondiente
            stock_row = (
                db.query(models.Stock)
                .filter(
                    models.Stock.articulo_cod == linea.articulo_cod,
                    models.Stock.ubicacion == linea.ubicacion_codigo
                )
                .first()
            )

            if stock_row:
                stock_row.cantidad = linea.cantidad_fisica
            else:
                # Crear nueva fila de stock si no existe
                nuevo_stock = models.Stock(
                    articulo_cod=linea.articulo_cod,
                    ubicacion=linea.ubicacion_codigo,
                    lote="",
                    cantidad=linea.cantidad_fisica,
                )
                db.add(nuevo_stock)

            ajustes_realizados += 1

        inv.estado = "cerrado"
        inv.cerrado_en = datetime.utcnow()
        db.commit()
        return {
            "mensaje": "Inventario cerrado con éxito",
            "ajustes_aplicados": ajustes_realizados
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Error al cerrar inventario: {str(e)}")
