from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal
from typing import Optional
from datetime import datetime
import models
from fastapi import HTTPException
from pydantic import BaseModel

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


class MovimientoInterno(BaseModel):
    producto_id: int
    cantidad: int
    ubicacion_origen_id: int
    ubicacion_destino_id: int
    motivo: Optional[str] = None

@router.post("/interno")
def crear_movimiento_interno(mov: MovimientoInterno, db: Session = Depends(get_db)):
    if mov.cantidad <= 0:
        raise HTTPException(400, "La cantidad debe ser mayor a 0")
        
    stock_origen = db.query(models.Stock).filter(
        models.Stock.producto_id == mov.producto_id,
        models.Stock.ubicacion_id == mov.ubicacion_origen_id
    ).first()

    if not stock_origen or stock_origen.cantidad < mov.cantidad:
        raise HTTPException(400, "Stock insuficiente en la ubicación de origen")

    stock_destino = db.query(models.Stock).filter(
        models.Stock.producto_id == mov.producto_id,
        models.Stock.ubicacion_id == mov.ubicacion_destino_id
    ).first()

    if not stock_destino:
        stock_destino = models.Stock(producto_id=mov.producto_id, ubicacion_id=mov.ubicacion_destino_id, cantidad=0)
        db.add(stock_destino)
        db.flush()

    cant_ant_ori = stock_origen.cantidad
    stock_origen.cantidad -= mov.cantidad
    stock_destino.cantidad += mov.cantidad

    db_mov = models.Movimiento(
        producto_id=mov.producto_id,
        ubicacion_origen_id=mov.ubicacion_origen_id,
        ubicacion_destino_id=mov.ubicacion_destino_id,
        tipo="transferencia",
        cantidad=mov.cantidad,
        cantidad_anterior=cant_ant_ori,
        cantidad_nueva=stock_origen.cantidad,
        motivo=mov.motivo or "Movimiento interno",
        fecha=datetime.utcnow()
    )
    db.add(db_mov)
    db.commit()
    
    return {"mensaje": "Transferencia realizada con éxito"}
