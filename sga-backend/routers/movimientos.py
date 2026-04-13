"""
Router de Movimientos — tabla ALBARANCS de LIN (esquema dbo).
Solo lectura — los movimientos se generan desde el sistema ERP legacy.
Cada fila de ALBARANCS es un movimiento de stock de un artículo.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from database import SessionLocal
import models

router = APIRouter(prefix="/movimientos", tags=["Movimientos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _mov_to_dict(m: models.MovimientoStock) -> dict:
    return {
        # Identificador compuesto para el frontend
        "id": f"{(m.serie or '').strip()}-{(m.ejercicio or '').strip()}-{m.numero}-{(m.mov or '').strip()}-{m.cod}",
        "serie": (m.serie or "").strip(),
        "ejercicio": (m.ejercicio or "").strip(),
        "numero": m.numero,
        "mov": (m.mov or "").strip(),
        "fecha": m.fecha.isoformat() if m.fecha else None,
        "hora": m.hora.isoformat() if m.hora else None,
        "articulo_cod": (m.articulo_cod or "").strip(),
        "cantidad": m.cantidad,
        "lote": (m.lote or "").strip(),
        "ubicacion": (m.ubicacion or "").strip(),
        "tipo_mov": (m.tipo_mov or "").strip(),
        "almacen_cod": (m.almacen_cod or "").strip(),
        "cliente_cod": (m.cliente_cod or "").strip() or None,
        "cliente_nom": (m.cliente_nom or "").strip() or None,
        "num_alb": (m.num_alb or "").strip() or None,
        "manual": m.manual,
    }


@router.get("/")
def listar_movimientos(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    articulo_cod: str = Query(None),
    ubicacion: str = Query(None),
    almacen_cod: str = Query(None),
    db: Session = Depends(get_db)
):
    """Lista movimientos de stock de la tabla ALBARANCS (solo lectura)."""
    query = db.query(models.MovimientoStock)

    if articulo_cod:
        query = query.filter(models.MovimientoStock.articulo_cod == articulo_cod)
    if ubicacion:
        query = query.filter(models.MovimientoStock.ubicacion == ubicacion)
    if almacen_cod:
        query = query.filter(models.MovimientoStock.almacen_cod == almacen_cod)

    total = query.count()
    movimientos = (
        query.order_by(desc(models.MovimientoStock.fecha))
        .offset(skip).limit(limit).all()
    )

    return {"total": total, "movimientos": [_mov_to_dict(m) for m in movimientos]}


@router.get("/recientes")
def movimientos_recientes(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Últimos movimientos de stock para el dashboard."""
    movimientos = (
        db.query(models.MovimientoStock)
        .order_by(desc(models.MovimientoStock.fecha))
        .limit(limit)
        .all()
    )
    return [_mov_to_dict(m) for m in movimientos]
