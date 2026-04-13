from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from datetime import datetime

router = APIRouter(prefix="/auditoria", tags=["Auditoria"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def log_auditoria(db: Session, usuario_id: int, accion: str, entidad: str, entidad_id: str = None, antes: str = None, despues: str = None, ip: str = None):
    log = models.AuditoriaLog(
        usuario_id=usuario_id,
        accion=accion,
        entidad=entidad,
        entidad_id=entidad_id,
        datos_antes=antes,
        datos_despues=despues,
        ip=ip,
        fecha=datetime.utcnow()
    )
    db.add(log)
    # No hace commit, asume que quien la llama la añade a su transacción o hace un flush
    
@router.get("/")
def listar_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = db.query(models.AuditoriaLog).order_by(models.AuditoriaLog.id.desc()).offset(skip).limit(limit).all()
    # Mapeo manual si queremos incluir usuario (opcional)
    resultado = []
    for l in logs:
        usuario = db.query(models.Usuario).filter(models.Usuario.id == l.usuario_id).first()
        resultado.append({
            "id": l.id,
            "fecha": l.fecha.isoformat(),
            "accion": l.accion,
            "entidad": l.entidad,
            "entidad_id": l.entidad_id,
            "datos_antes": l.datos_antes,
            "datos_despues": l.datos_despues,
            "ip": l.ip,
            "usuario": usuario.email if usuario else "Sistema"
        })
    return resultado
