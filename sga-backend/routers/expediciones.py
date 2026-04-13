"""
Router de Expediciones — tablas propias del SGA (esquema sga).
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import modelos_operacionales as op
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


def _exp_to_dict(e: op.Expedicion) -> dict:
    return {
        "id": e.id,
        "codigo": e.codigo,
        "picking_id": e.picking_id,
        "estado": e.estado,
        "agencia_transporte": e.agencia_transporte,
        "tracking_number": e.tracking_number,
        "creado_en": e.creado_en.isoformat() if e.creado_en else None,
        "fecha_envio": e.fecha_envio.isoformat() if e.fecha_envio else None,
    }


@router.get("/")
def listar_expediciones(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    expediciones = (
        db.query(op.Expedicion)
        .order_by(op.Expedicion.id.desc())
        .offset(skip).limit(limit).all()
    )
    return [_exp_to_dict(e) for e in expediciones]


@router.post("/", status_code=201)
def crear_expedicion(item: dict, db: Session = Depends(get_db)):
    """
    Body esperado:
    {"picking_id": 1, "agencia_transporte": "MRW", "tracking_number": "XYZ123"}
    """
    picking_id = item.get("picking_id")
    if picking_id:
        pik = db.query(op.PickingOrden).filter(op.PickingOrden.id == picking_id).first()
        if not pik or pik.estado != "completado":
            raise HTTPException(400, "El picking asociado no existe o no está completado")

    exp = op.Expedicion(
        codigo=_generar_codigo(),
        picking_id=picking_id,
        agencia_transporte=item.get("agencia_transporte"),
        tracking_number=item.get("tracking_number"),
        estado="preparacion",
    )
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return _exp_to_dict(exp)


@router.put("/{exp_id}/procesar")
def procesar_expedicion(
    exp_id: int,
    agencia: str = None,
    tracking: str = None,
    db: Session = Depends(get_db)
):
    exp = db.query(op.Expedicion).filter(op.Expedicion.id == exp_id).first()
    if not exp:
        raise HTTPException(404, "Expedición no encontrada")

    if agencia:
        exp.agencia_transporte = agencia
    if tracking:
        exp.tracking_number = tracking

    exp.estado = "enviada"
    exp.fecha_envio = datetime.utcnow()
    db.commit()
    return {"mensaje": "Expedición marcada como enviada", "expedicion": _exp_to_dict(exp)}
