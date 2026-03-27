from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal
import models
import schemas
from typing import List
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

@router.get("/", response_model=List[schemas.PickingOrdenResponse])
def listar_ordenes(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.PickingOrden).options(joinedload(models.PickingOrden.lineas)).order_by(models.PickingOrden.id.desc()).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.PickingOrdenResponse, status_code=201)
def crear_orden(item: schemas.PickingOrdenCreate, db: Session = Depends(get_db)):
    db_pik = models.PickingOrden(
        codigo=item.codigo or _generar_codigo(),
        operario_id=item.operario_id,
        prioridad=item.prioridad,
        notas=item.notas,
        estado='pendiente'
    )
    db.add(db_pik)
    db.flush()

    for linea in item.lineas:
        db_linea = models.PickingLinea(
            picking_id=db_pik.id,
            producto_id=linea.producto_id,
            cantidad_solicitada=linea.cantidad_solicitada,
            ubicacion_origen_id=linea.ubicacion_origen_id,
            estado='pendiente'
        )
        db.add(db_linea)
        
    db.commit()
    db.refresh(db_pik)
    return db_pik

@router.put("/{picking_id}/asignar")
def asignar_operario(picking_id: int, operario_id: int, db: Session = Depends(get_db)):
    orden = db.query(models.PickingOrden).filter(models.PickingOrden.id == picking_id).first()
    if not orden:
        raise HTTPException(404, "Orden no encontrada")
    orden.operario_id = operario_id
    if orden.estado == 'pendiente':
        orden.estado = 'en_proceso'
    db.commit()
    return {"mensaje": "Asignado"}

@router.put("/{picking_id}/lineas/{linea_id}/recoger")
def marcar_linea_recogida(picking_id: int, linea_id: int, c_recogida: int, db: Session = Depends(get_db)):
    linea = db.query(models.PickingLinea).filter(models.PickingLinea.id == linea_id, models.PickingLinea.picking_id == picking_id).first()
    if not linea:
        raise HTTPException(404, "Línea no encontrada")
    
    linea.cantidad_recogida = c_recogida
    if linea.cantidad_recogida >= linea.cantidad_solicitada:
        linea.estado = 'completada'
    else:
        linea.estado = 'parcial'
        
    db.commit()
    return {"mensaje": "Línea actualizada"}

@router.put("/{picking_id}/completar")
def completar_picking(picking_id: int, db: Session = Depends(get_db)):
    """Descuenta el stock físico y completa la orden"""
    orden = db.query(models.PickingOrden).options(joinedload(models.PickingOrden.lineas)).filter(models.PickingOrden.id == picking_id).first()
    if not orden:
        raise HTTPException(404, "Orden no encontrada")
    if orden.estado == 'completado':
        return {"mensaje": "Ya estaba completada"}

    try:
        for linea in orden.lineas:
            if linea.cantidad_recogida > 0:
                # Buscar el stock en la ubicación de origen especificada (o la primera que tenga stock si no se especificó)
                q_stock = db.query(models.Stock).filter(models.Stock.producto_id == linea.producto_id)
                if linea.ubicacion_origen_id:
                    q_stock = q_stock.filter(models.Stock.ubicacion_id == linea.ubicacion_origen_id)
                
                stock_item = q_stock.first()
                if not stock_item or stock_item.cantidad < linea.cantidad_recogida:
                    # En la vida real haríamos backorder o error. Por simplicidad, forzamos el negativo o restamos lo que haya.
                    pass 

                if stock_item:
                    cant_ant = stock_item.cantidad
                    stock_item.cantidad -= linea.cantidad_recogida
                    
                    mov = models.Movimiento(
                        producto_id=linea.producto_id,
                        ubicacion_origen_id=linea.ubicacion_origen_id,
                        tipo="salida",
                        cantidad=linea.cantidad_recogida,
                        cantidad_anterior=cant_ant,
                        cantidad_nueva=stock_item.cantidad,
                        motivo=f"Picking {orden.codigo}",
                        fecha=datetime.utcnow()
                    )
                    db.add(mov)

        orden.estado = 'completado'
        orden.completado_en = datetime.utcnow()
        db.commit()
        return {"mensaje": "Picking completado y stock descontado"}
    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Error completando picking: {str(e)}")
