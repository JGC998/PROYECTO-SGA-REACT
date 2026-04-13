"""
Router de Ubicaciones — tabla UBICACION de LIN (esquema dbo).
PK: UBICON (float). El código legible es UBICODUBI.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
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


def _ubicacion_to_dict(u: models.Ubicacion, cantidad: float = 0.0) -> dict:
    return {
        "id": u.id,
        "codigo": (u.codigo or "").strip(),
        "nombre": (u.nombre or "").strip(),
        "descripcion": (u.nombre or "").strip(),  # alias para compatibilidad
        "almacen_cod": (u.almacen_cod or "").strip(),
        "alto": u.alto,
        "ancho": u.ancho,
        "num_palets": u.num_palets,
        "libre": u.libre,
        "activo": True,
        "cantidad_total": cantidad,
    }


@router.get("/")
def listar_ubicaciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    almacen_cod: str = Query(None, description="Filtra por código de almacén"),
    busqueda: str = Query(None, description="Filtra por código o nombre de ubicación"),
    db: Session = Depends(get_db)
):
    """Lista ubicaciones con stock total calculado."""
    query = db.query(models.Ubicacion)

    if almacen_cod:
        query = query.filter(models.Ubicacion.almacen_cod == almacen_cod)
    if busqueda:
        like = f"%{busqueda}%"
        query = query.filter(
            models.Ubicacion.codigo.ilike(like) |
            models.Ubicacion.nombre.ilike(like)
        )

    total = query.count()
    ubicaciones = query.order_by(models.Ubicacion.codigo).offset(skip).limit(limit).all()

    # Calcular cantidad total en cada ubicación (por código STOUBI)
    codigos = [u.codigo.strip() for u in ubicaciones if u.codigo]
    stock_map = {}
    if codigos:
        stock_rows = (
            db.query(models.Stock.ubicacion, func.sum(models.Stock.cantidad))
            .filter(models.Stock.ubicacion.in_(codigos))
            .group_by(models.Stock.ubicacion)
            .all()
        )
        stock_map = {row[0].strip(): (row[1] or 0.0) for row in stock_rows}

    resultado = [
        _ubicacion_to_dict(u, stock_map.get((u.codigo or "").strip(), 0.0))
        for u in ubicaciones
    ]
    return {"total": total, "ubicaciones": resultado}


@router.get("/{ubicacion_id}")
def obtener_ubicacion(ubicacion_id: float, db: Session = Depends(get_db)):
    """Obtiene una ubicación por su UBICON (id numérico)."""
    ubicacion = db.query(models.Ubicacion).filter(models.Ubicacion.id == ubicacion_id).first()
    if not ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")

    cantidad = (
        db.query(func.sum(models.Stock.cantidad))
        .filter(models.Stock.ubicacion == (ubicacion.codigo or "").strip())
        .scalar()
    ) or 0.0

    return _ubicacion_to_dict(ubicacion, cantidad)


@router.post("/", status_code=201)
def crear_ubicacion(item: UbicacionCreate, db: Session = Depends(get_db)):
    """Crea una nueva ubicación. El UBICON se genera automáticamente por LIN."""
    existe = db.query(models.Ubicacion).filter(
        models.Ubicacion.codigo == item.codigo
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail=f"El código de ubicación '{item.codigo}' ya existe")

    # Obtener el próximo UBICON disponible
    max_id = db.query(func.max(models.Ubicacion.id)).scalar() or 0
    nuevo_id = max_id + 1

    nueva = models.Ubicacion(
        id=nuevo_id,
        codigo=item.codigo.strip().upper(),
        nombre=item.nombre or "",
        almacen_cod=item.almacen_cod or "",
        alto=item.alto or 0,
        ancho=item.ancho or 0,
        num_palets=item.num_palets or 1,
        libre=0,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return _ubicacion_to_dict(nueva)


@router.put("/{ubicacion_id}")
def actualizar_ubicacion(ubicacion_id: float, item: UbicacionCreate, db: Session = Depends(get_db)):
    """Actualiza los datos de una ubicación."""
    ubicacion = db.query(models.Ubicacion).filter(models.Ubicacion.id == ubicacion_id).first()
    if not ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")

    ubicacion.codigo = item.codigo.strip().upper()
    ubicacion.nombre = item.nombre or ""
    ubicacion.almacen_cod = item.almacen_cod or ""
    if item.alto is not None:
        ubicacion.alto = item.alto
    if item.ancho is not None:
        ubicacion.ancho = item.ancho
    if item.num_palets is not None:
        ubicacion.num_palets = item.num_palets

    db.commit()
    db.refresh(ubicacion)
    return _ubicacion_to_dict(ubicacion)


@router.delete("/{ubicacion_id}")
def eliminar_ubicacion(ubicacion_id: float, db: Session = Depends(get_db)):
    """Elimina una ubicación si no tiene stock."""
    ubicacion = db.query(models.Ubicacion).filter(models.Ubicacion.id == ubicacion_id).first()
    if not ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")

    codigo = (ubicacion.codigo or "").strip()
    stock_en_ubi = (
        db.query(func.sum(models.Stock.cantidad))
        .filter(models.Stock.ubicacion == codigo)
        .scalar()
    ) or 0.0

    if stock_en_ubi > 0:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede borrar la ubicación '{codigo}': tiene {stock_en_ubi} unidades en stock"
        )

    db.delete(ubicacion)
    db.commit()
    return {"message": f"Ubicación '{codigo}' eliminada"}


@router.get("/{ubicacion_id}/stock")
def stock_en_ubicacion(ubicacion_id: float, db: Session = Depends(get_db)):
    """Lista el stock detallado (por artículo y lote) de una ubicación."""
    ubicacion = db.query(models.Ubicacion).filter(models.Ubicacion.id == ubicacion_id).first()
    if not ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")

    codigo = (ubicacion.codigo or "").strip()
    stock_rows = (
        db.query(models.Stock)
        .filter(models.Stock.ubicacion == codigo, models.Stock.cantidad > 0)
        .all()
    )

    return {
        "ubicacion_id": ubicacion_id,
        "codigo": codigo,
        "nombre": (ubicacion.nombre or "").strip(),
        "stock": [
            {
                "articulo_cod": s.articulo_cod.strip(),
                "lote": s.lote.strip(),
                "cantidad": s.cantidad,
            }
            for s in stock_rows
        ]
    }
