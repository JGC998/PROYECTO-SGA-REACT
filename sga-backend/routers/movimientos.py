from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal
from typing import Optional
import models

router = APIRouter(prefix="/movimientos", tags=["Movimientos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def listar_movimientos(
    skip: int = 0,
    limit: int = 50,
    producto_id: Optional[int] = Query(None),
    tipo: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(models.Movimiento).options(
        joinedload(models.Movimiento.producto)
    )

    if producto_id is not None:
        query = query.filter(models.Movimiento.producto_id == producto_id)
    if tipo is not None:
        query = query.filter(models.Movimiento.tipo == tipo)

    total = query.count()
    movimientos = (
        query.order_by(models.Movimiento.fecha.desc()).offset(skip).limit(limit).all()
    )

    resultado = []
    for m in movimientos:
        resultado.append({
            "id": m.id,
            "producto_id": m.producto_id,
            "producto_nombre": m.producto.nombre if m.producto else None,
            "producto_sku": m.producto.sku if m.producto else None,
            "tipo": m.tipo,
            "cantidad": m.cantidad,
            "cantidad_anterior": m.cantidad_anterior,
            "cantidad_nueva": m.cantidad_nueva,
            "motivo": m.motivo,
            "fecha": m.fecha.isoformat(),
        })
    return {"total": total, "movimientos": resultado}
