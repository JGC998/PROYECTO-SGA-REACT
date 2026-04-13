"""
Router de Almacenes — tabla ALMACENES de LIN (esquema dbo).
PK: ALMCOD (str de 2 chars). No existe tabla de Zonas en LIN — la jerarquía es Almacén → Ubicación.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from schemas import AlmacenCreate

router = APIRouter(prefix="/almacenes", tags=["Almacenes"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _almacen_to_dict(almacen: models.Almacen, num_ubicaciones: int = 0) -> dict:
    return {
        "id": almacen.codigo,
        "codigo": almacen.codigo,
        "nombre": (almacen.nombre or "").strip(),
        "activo": True,
        "num_ubicaciones": num_ubicaciones,
        # Campos de compatibilidad con frontend antiguo
        "direccion": None,
    }


@router.get("/")
def listar_almacenes(db: Session = Depends(get_db)):
    """Lista todos los almacenes de la tabla ALMACENES."""
    almacenes = db.query(models.Almacen).order_by(models.Almacen.codigo).all()

    resultado = []
    for a in almacenes:
        num_ubi = (
            db.query(models.Ubicacion)
            .filter(models.Ubicacion.almacen_cod == a.codigo)
            .count()
        )
        resultado.append(_almacen_to_dict(a, num_ubi))

    return resultado


@router.get("/{codigo}")
def obtener_almacen(codigo: str, db: Session = Depends(get_db)):
    """Obtiene un almacén por su código ALMCOD."""
    almacen = db.query(models.Almacen).filter(models.Almacen.codigo == codigo).first()
    if not almacen:
        raise HTTPException(status_code=404, detail=f"Almacén '{codigo}' no encontrado")

    num_ubi = (
        db.query(models.Ubicacion)
        .filter(models.Ubicacion.almacen_cod == codigo)
        .count()
    )
    return _almacen_to_dict(almacen, num_ubi)


@router.post("/", status_code=201)
def crear_almacen(item: AlmacenCreate, db: Session = Depends(get_db)):
    """Crea un nuevo almacén en la tabla ALMACENES."""
    existe = db.query(models.Almacen).filter(models.Almacen.codigo == item.codigo).first()
    if existe:
        raise HTTPException(status_code=400, detail=f"El código de almacén '{item.codigo}' ya existe")

    nuevo = models.Almacen(
        codigo=item.codigo.strip().upper(),
        nombre=item.nombre.strip(),
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return _almacen_to_dict(nuevo)


@router.put("/{codigo}")
def actualizar_almacen(codigo: str, item: AlmacenCreate, db: Session = Depends(get_db)):
    """Actualiza el nombre de un almacén."""
    almacen = db.query(models.Almacen).filter(models.Almacen.codigo == codigo).first()
    if not almacen:
        raise HTTPException(status_code=404, detail=f"Almacén '{codigo}' no encontrado")

    almacen.nombre = item.nombre.strip()
    db.commit()
    db.refresh(almacen)
    return _almacen_to_dict(almacen)


@router.delete("/{codigo}")
def eliminar_almacen(codigo: str, db: Session = Depends(get_db)):
    """Elimina un almacén si no tiene ubicaciones con stock."""
    almacen = db.query(models.Almacen).filter(models.Almacen.codigo == codigo).first()
    if not almacen:
        raise HTTPException(status_code=404, detail=f"Almacén '{codigo}' no encontrado")

    # Comprobar si hay stock en sus ubicaciones
    ubi_con_stock = (
        db.query(models.Stock)
        .join(models.Ubicacion, models.Stock.ubicacion == models.Ubicacion.codigo)
        .filter(models.Ubicacion.almacen_cod == codigo, models.Stock.cantidad > 0)
        .count()
    )
    if ubi_con_stock > 0:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede borrar el almacén '{codigo}': tiene ubicaciones con stock"
        )

    db.delete(almacen)
    db.commit()
    return {"message": f"Almacén '{codigo}' eliminado"}


# Ubicaciones dentro de un almacén (reemplaza el antiguo endpoint de Zonas)
@router.get("/{codigo}/ubicaciones")
def listar_ubicaciones_almacen(codigo: str, db: Session = Depends(get_db)):
    """Lista todas las ubicaciones de un almacén concreto."""
    almacen = db.query(models.Almacen).filter(models.Almacen.codigo == codigo).first()
    if not almacen:
        raise HTTPException(status_code=404, detail=f"Almacén '{codigo}' no encontrado")

    ubicaciones = (
        db.query(models.Ubicacion)
        .filter(models.Ubicacion.almacen_cod == codigo)
        .order_by(models.Ubicacion.codigo)
        .all()
    )
    return [
        {
            "id": u.id,
            "codigo": (u.codigo or "").strip(),
            "nombre": (u.nombre or "").strip(),
            "almacen_cod": (u.almacen_cod or "").strip(),
            "alto": u.alto,
            "ancho": u.ancho,
            "num_palets": u.num_palets,
            "libre": u.libre,
        }
        for u in ubicaciones
    ]
