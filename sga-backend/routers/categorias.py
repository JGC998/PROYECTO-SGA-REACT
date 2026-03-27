from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from schemas import CategoriaCreate, CategoriaResponse
from auth.dependencies import get_current_user

router = APIRouter(prefix="/categorias", tags=["Categorías"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db), 
                      current_user: models.Usuario = Depends(get_current_user)):
    return db.query(models.Categoria).all()


@router.post("/", response_model=CategoriaResponse)
def crear_categoria(item: CategoriaCreate, db: Session = Depends(get_db),
                    current_user: models.Usuario = Depends(get_current_user)):
    nueva = models.Categoria(**item.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva
