"""
Router de Categorías — tabla SUBFAMILIA de LIN (esquema dbo).
En LIN, las categorías/familias de artículos se llaman SUBFAMILIA.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from schemas import CategoriaCreate, CategoriaResponse

router = APIRouter(prefix="/categorias", tags=["Categorías"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def listar_categorias(db: Session = Depends(get_db)):
    """Lista todas las subfamilias/categorías de artículos."""
    cats = db.query(models.SubFamilia).order_by(models.SubFamilia.nombre).all()
    return [
        {"id": c.codigo, "codigo": c.codigo, "nombre": (c.nombre or "").strip()}
        for c in cats
    ]


@router.post("/", status_code=201)
def crear_categoria(item: CategoriaCreate, db: Session = Depends(get_db)):
    """Crea una nueva subfamilia/categoría."""
    existe = db.query(models.SubFamilia).filter(models.SubFamilia.codigo == item.codigo).first()
    if existe:
        raise HTTPException(status_code=400, detail=f"El código '{item.codigo}' ya existe")

    nueva = models.SubFamilia(codigo=item.codigo.strip(), nombre=item.nombre.strip())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return {"id": nueva.codigo, "codigo": nueva.codigo, "nombre": (nueva.nombre or "").strip()}


@router.delete("/{codigo}")
def eliminar_categoria(codigo: str, db: Session = Depends(get_db)):
    """Elimina una categoría."""
    cat = db.query(models.SubFamilia).filter(models.SubFamilia.codigo == codigo).first()
    if not cat:
        raise HTTPException(status_code=404, detail=f"Categoría '{codigo}' no encontrada")
    db.delete(cat)
    db.commit()
    return {"message": f"Categoría '{codigo}' eliminada"}
