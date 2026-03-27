from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal
import models

router = APIRouter(prefix="/reportes", tags=["Reportes"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/stock-bajo")
def stock_bajo(db: Session = Depends(get_db)):
    """Productos cuya cantidad de stock está por debajo del stock_minimo."""
    productos = (
        db.query(models.Producto)
        .options(joinedload(models.Producto.stock))
        .all()
    )
    resultado = []
    for p in productos:
        cantidad = p.stock.cantidad if p.stock else 0
        if cantidad < p.stock_minimo:
            resultado.append({
                "id": p.id,
                "sku": p.sku,
                "nombre": p.nombre,
                "stock_minimo": p.stock_minimo,
                "cantidad": cantidad,
                "deficit": p.stock_minimo - cantidad,
            })
    return resultado


@router.get("/resumen")
def resumen(db: Session = Depends(get_db)):
    """Métricas generales del almacén."""
    productos = (
        db.query(models.Producto)
        .options(joinedload(models.Producto.stock))
        .all()
    )
    total_productos = len(productos)
    bajo_minimo = sum(
        1 for p in productos
        if (p.stock.cantidad if p.stock else 0) < p.stock_minimo
    )

    ultimos = (
        db.query(models.Movimiento)
        .options(joinedload(models.Movimiento.producto))
        .order_by(models.Movimiento.fecha.desc())
        .limit(5)
        .all()
    )
    movimientos_recientes = [
        {
            "id": m.id,
            "producto_nombre": m.producto.nombre if m.producto else None,
            "tipo": m.tipo,
            "cantidad": m.cantidad,
            "fecha": m.fecha.isoformat(),
        }
        for m in ultimos
    ]

    return {
        "total_productos": total_productos,
        "productos_bajo_minimo": bajo_minimo,
        "ultimos_movimientos": movimientos_recientes,
    }
