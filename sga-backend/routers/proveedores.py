from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from schemas import ProveedorCreate, ProveedorResponse
from auth.dependencies import get_current_user

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[ProveedorResponse])
def listar_proveedores(db: Session = Depends(get_db), 
                       current_user: models.Usuario = Depends(get_current_user)):
    return db.query(models.Proveedor).all()


@router.post("/", response_model=ProveedorResponse)
def crear_proveedor(item: ProveedorCreate, db: Session = Depends(get_db),
                    current_user: models.Usuario = Depends(get_current_user)):
    if item.cif:
        existe = db.query(models.Proveedor).filter(models.Proveedor.cif == item.cif).first()
        if existe:
            raise HTTPException(status_code=400, detail="Un proveedor con este CIF ya existe")

    nuevo = models.Proveedor(**item.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
