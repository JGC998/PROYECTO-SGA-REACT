"""
Router de Proveedores — tabla PROVEEDOR de LIN (esquema dbo).
PK compuesta: (CLICOD, CLICENCOD). Se usa CLICOD como identificador en la API.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from schemas import ProveedorCreate

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _proveedor_to_dict(p: models.Proveedor) -> dict:
    return {
        "id": (p.cod or "").strip(),
        "cod": (p.cod or "").strip(),
        "cen_cod": (p.cen_cod or "").strip(),
        "nombre": (p.nombre or "").strip(),
        "razon": (p.razon or "").strip(),
        "nif": (p.nif or "").strip() or None,
        "cif": (p.nif or "").strip() or None,      # alias
        "telefono": (p.telefono or "").strip() or None,
        "email": (p.email or "").strip() or None,
        "contacto": (p.contacto or "").strip() or None,
        "cargo": (p.cargo or "").strip() or None,
        "direccion": (p.direccion or "").strip() or None,
        "ciudad": (p.ciudad or "").strip() or None,
        "provincia": (p.provincia or "").strip() or None,
        "cp": (p.cp or "").strip() or None,
        "pais": (p.pais or "").strip() or None,
        "activo": True,
    }


@router.get("/")
def listar_proveedores(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    busqueda: str = Query(None),
    db: Session = Depends(get_db)
):
    """Lista proveedores de la tabla PROVEEDOR."""
    query = db.query(models.Proveedor)

    if busqueda:
        like = f"%{busqueda}%"
        query = query.filter(
            models.Proveedor.nombre.ilike(like) |
            models.Proveedor.razon.ilike(like) |
            models.Proveedor.cod.ilike(like)
        )

    total = query.count()
    proveedores = query.order_by(models.Proveedor.nombre).offset(skip).limit(limit).all()
    return {"total": total, "proveedores": [_proveedor_to_dict(p) for p in proveedores]}


@router.get("/{cod}")
def obtener_proveedor(cod: str, db: Session = Depends(get_db)):
    """Obtiene un proveedor por su CLICOD."""
    proveedor = db.query(models.Proveedor).filter(models.Proveedor.cod == cod).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail=f"Proveedor '{cod}' no encontrado")
    return _proveedor_to_dict(proveedor)


@router.post("/", status_code=201)
def crear_proveedor(item: ProveedorCreate, db: Session = Depends(get_db)):
    """Crea un nuevo proveedor en la tabla PROVEEDOR."""
    existe = db.query(models.Proveedor).filter(
        models.Proveedor.cod == item.cod,
        models.Proveedor.cen_cod == item.cen_cod
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail=f"El proveedor '{item.cod}' ya existe")

    nuevo = models.Proveedor(
        cod=item.cod.strip(),
        cen_cod=item.cen_cod.strip(),
        razon=item.razon or "",
        nombre=item.nombre.strip(),
        nif=item.nif or "",
        telefono=item.telefono or "",
        email=item.email or "",
        contacto=item.contacto or "",
        direccion=item.direccion or "",
        ciudad=item.ciudad or "",
        provincia=item.provincia or "",
        cp=item.cp or "",
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return _proveedor_to_dict(nuevo)


@router.put("/{cod}")
def actualizar_proveedor(cod: str, item: ProveedorCreate, db: Session = Depends(get_db)):
    """Actualiza los datos de un proveedor."""
    proveedor = db.query(models.Proveedor).filter(models.Proveedor.cod == cod).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail=f"Proveedor '{cod}' no encontrado")

    proveedor.razon = item.razon or proveedor.razon
    proveedor.nombre = item.nombre.strip()
    proveedor.nif = item.nif or proveedor.nif
    proveedor.telefono = item.telefono or proveedor.telefono
    proveedor.email = item.email or proveedor.email
    proveedor.contacto = item.contacto or proveedor.contacto
    proveedor.direccion = item.direccion or proveedor.direccion
    proveedor.ciudad = item.ciudad or proveedor.ciudad
    proveedor.provincia = item.provincia or proveedor.provincia
    proveedor.cp = item.cp or proveedor.cp

    db.commit()
    db.refresh(proveedor)
    return _proveedor_to_dict(proveedor)


@router.delete("/{cod}")
def eliminar_proveedor(cod: str, db: Session = Depends(get_db)):
    """Elimina un proveedor de la tabla PROVEEDOR."""
    proveedor = db.query(models.Proveedor).filter(models.Proveedor.cod == cod).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail=f"Proveedor '{cod}' no encontrado")

    db.delete(proveedor)
    db.commit()
    return {"message": f"Proveedor '{cod}' eliminado"}
