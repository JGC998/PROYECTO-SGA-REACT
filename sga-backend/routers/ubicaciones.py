from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from schemas import UbicacionCreate

router = APIRouter(prefix="/ubicaciones", tags=["Ubicaciones"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def listar_ubicaciones(db: Session = Depends(get_db)):
    return db.query(models.Ubicacion).all()


@router.post("/", status_code=201)
def crear_ubicacion(item: UbicacionCreate, db: Session = Depends(get_db)):
    existe = db.query(models.Ubicacion).filter(
        models.Ubicacion.codigo == item.codigo
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ese código de ubicación ya existe")

    nueva = models.Ubicacion(
        codigo=item.codigo.strip(),
        descripcion=item.descripcion,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva
