from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal
import models
import schemas
from typing import List
from datetime import datetime

router = APIRouter(prefix="/expediciones", tags=["Expediciones"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def _generar_codigo() -> str:
    return f"EXP-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"

@router.get("/", response_model=List[schemas.ExpedicionResponse])
def listar_expediciones(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Expedicion).order_by(models.Expedicion.id.desc()).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.ExpedicionResponse, status_code=201)
def crear_expedicion(item: schemas.ExpedicionCreate, db: Session = Depends(get_db)):
    # Validamos si viene de un picking (opcional)
    if item.picking_id:
        pik = db.query(models.PickingOrden).filter(models.PickingOrden.id == item.picking_id).first()
        if not pik or pik.estado != 'completado':
            raise HTTPException(400, "El picking asociado no existe o no está completado")
            
    db_exp = models.Expedicion(
        codigo=item.codigo or _generar_codigo(),
        picking_id=item.picking_id,
        agencia_transporte=item.agencia_transporte,
        tracking_number=item.tracking_number,
        estado='preparacion'
    )
    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)
    return db_exp

@router.put("/{exp_id}/procesar")
def procesar_expedicion(exp_id: int, agencia: str = None, tracking: str = None, db: Session = Depends(get_db)):
    exp = db.query(models.Expedicion).filter(models.Expedicion.id == exp_id).first()
    if not exp:
        raise HTTPException(404, "Expedición no encontrada")
    
    if agencia: exp.agencia_transporte = agencia
    if tracking: exp.tracking_number = tracking
    
    exp.estado = 'enviada'
    exp.fecha_envio = datetime.utcnow()
    db.commit()
    return {"mensaje": "Expedición marcada como enviada"}
