from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from schemas import AlmacenCreate, AlmacenResponse, ZonaResponse, ZonaCreate
from auth.dependencies import get_current_user

router = APIRouter(prefix="/almacenes", tags=["Almacenes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[AlmacenResponse])
def listar_almacenes(db: Session = Depends(get_db), 
                     current_user: models.Usuario = Depends(get_current_user)):
    return db.query(models.Almacen).all()

@router.post("/", response_model=AlmacenResponse)
def crear_almacen(item: AlmacenCreate, db: Session = Depends(get_db),
                  current_user: models.Usuario = Depends(get_current_user)):
    existe = db.query(models.Almacen).filter(models.Almacen.codigo == item.codigo).first()
    if existe:
         raise HTTPException(status_code=400, detail="El código de almacén ya existe")
         
    nuevo = models.Almacen(**item.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/{almacen_id}/zonas", response_model=list[ZonaResponse])
def listar_zonas_almacen(almacen_id: int, db: Session = Depends(get_db),
                         current_user: models.Usuario = Depends(get_current_user)):
    return db.query(models.Zona).filter(models.Zona.almacen_id == almacen_id).all()

@router.post("/{almacen_id}/zonas", response_model=ZonaResponse)
def crear_zona(almacen_id: int, item: ZonaCreate, db: Session = Depends(get_db),
               current_user: models.Usuario = Depends(get_current_user)):
    almacen = db.query(models.Almacen).filter(models.Almacen.id == almacen_id).first()
    if not almacen:
        raise HTTPException(status_code=404, detail="Almacén no encontrado")
        
    item.almacen_id = almacen_id
    nueva_zona = models.Zona(**item.model_dump())
    db.add(nueva_zona)
    db.commit()
    db.refresh(nueva_zona)
    return nueva_zona
