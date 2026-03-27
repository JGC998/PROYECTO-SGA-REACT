from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from datetime import datetime

router = APIRouter(prefix="/stock", tags=["Stock"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _get_o_crear_stock(producto_id: int, db: Session) -> models.Stock:
    """Devuelve el registro de stock o lo crea si no existe."""
    item = db.query(models.Stock).filter(models.Stock.producto_id == producto_id).first()
    if not item:
        item = models.Stock(producto_id=producto_id, ubicacion_id=None, cantidad=0)
        db.add(item)
        db.flush()
    return item


def _registrar_movimiento(db: Session, producto_id: int, cambio: int,
                           cantidad_anterior: int, cantidad_nueva: int,
                           motivo: str = None):
    mov = models.Movimiento(
        producto_id=producto_id,
        tipo="entrada" if cambio > 0 else "salida",
        cantidad=abs(cambio),
        cantidad_anterior=cantidad_anterior,
        cantidad_nueva=cantidad_nueva,
        motivo=motivo,
        fecha=datetime.utcnow(),
    )
    db.add(mov)


@router.put("/{producto_id}")
def actualizar_cantidad(producto_id: int, cambio: int, motivo: str = None,
                        db: Session = Depends(get_db)):
    # Verificar que el producto existe
    if not db.query(models.Producto).filter(models.Producto.id == producto_id).first():
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    try:
        item = _get_o_crear_stock(producto_id, db)
        cantidad_anterior = item.cantidad
        item.cantidad = max(0, item.cantidad + cambio)

        _registrar_movimiento(db, producto_id, cambio,
                               cantidad_anterior, item.cantidad, motivo)
        db.commit()
        return {"nueva_cantidad": item.cantidad}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.put("/{producto_id}/fijar")
def fijar_cantidad(producto_id: int, cantidad: int, motivo: str = None,
                   db: Session = Depends(get_db)):
    if not db.query(models.Producto).filter(models.Producto.id == producto_id).first():
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    try:
        item = _get_o_crear_stock(producto_id, db)
        cantidad_anterior = item.cantidad
        cantidad_nueva = max(0, cantidad)
        cambio = cantidad_nueva - cantidad_anterior
        item.cantidad = cantidad_nueva

        if cambio != 0:
            _registrar_movimiento(db, producto_id, cambio,
                                   cantidad_anterior, cantidad_nueva, motivo)
        db.commit()
        return {"nueva_cantidad": item.cantidad}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/mapa/{zona_id}")
def obtener_mapa_zona(zona_id: int, db: Session = Depends(get_db)):
    """
    Devuelve las ubicaciones de una zona con el nivel de ocupación actual.
    Por simplicidad, asume que si hay items en el stock vinculados a esa ubicación, esa es la ocupación.
    """
    zona = db.query(models.Zona).filter(models.Zona.id == zona_id).first()
    if not zona:
        raise HTTPException(status_code=404, detail="Zona no encontrada")

    ubicaciones = db.query(models.Ubicacion).filter(models.Ubicacion.zona_id == zona_id).all()
    
    resultado = {
        "zona_id": zona.id,
        "zona_nombre": zona.nombre,
        "ubicaciones": []
    }

    for u in ubicaciones:
        stock_en_ubicacion = db.query(models.Stock).filter(models.Stock.ubicacion_id == u.id).all()
        cantidad_total = sum(s.cantidad for s in stock_en_ubicacion)
        
        capacidad = u.capacidad_max if u.capacidad_max else 100 # Default si no está definido
        porcentaje = round((cantidad_total / capacidad) * 100, 2) if capacidad > 0 else 0
        
        resultado["ubicaciones"].append({
            "id": u.id,
            "codigo": u.codigo,
            "capacidad_max": capacidad,
            "cantidad_actual": cantidad_total,
            "ocupacion_porcentaje": min(100, porcentaje),
            "estado": "lleno" if porcentaje >= 100 else "medio" if porcentaje >= 50 else "vacio",
            "activo": u.activo
        })
        
    return resultado
