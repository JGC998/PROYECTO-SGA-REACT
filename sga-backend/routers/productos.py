"""
Router de Artículos — tabla ARTICULO de LIN (esquema dbo).
PK: ARTCOD (str). La cantidad total se calcula sumando STOCK.STOCAN.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal
import models
from schemas import ArticuloCreate, ArticuloUpdate

router = APIRouter(prefix="/productos", tags=["Productos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _articulo_to_dict(articulo: models.Articulo, cantidad: float = 0.0) -> dict:
    """Convierte un modelo Articulo a un dict con la estructura que espera el frontend."""
    return {
        "id": articulo.sku,          # Alias str para compatibilidad frontend
        "sku": articulo.sku,
        "nombre": (articulo.nombre or "").strip(),
        "codigo2": (articulo.codigo2 or "").strip() or None,
        "barcode": (articulo.barcode or "").strip() or None,
        "barcode_caja": (articulo.barcode_caja or "").strip() or None,
        "barcode_palet": (articulo.barcode_palet or "").strip() or None,
        "codigo_largo": (articulo.codigo_largo or "").strip() or None,
        "peso_uni": articulo.peso_uni,
        "stock_min": articulo.stock_min,
        "stock_max": articulo.stock_max,
        # Campos de compatibilidad con el frontend antiguo
        "stock_minimo": articulo.stock_min,
        "stock_maximo": articulo.stock_max,
        "precio_coste": articulo.precio_coste,
        "grupo": (articulo.grupo or "").strip() or None,
        "unidad_medida": (articulo.unidad_medida or "").strip() or None,
        "material": (articulo.material or "").strip() or None,
        "color": (articulo.color or "").strip() or None,
        "imagen_url": (articulo.imagen_url or "").strip() or None,
        "activo": articulo.activo,
        "oculto": articulo.oculto,
        "cantidad": cantidad,
        # No existe creado_en en LIN — ponemos None
        "categoria_id": None,
        "proveedor_id": None,
        "creado_en": None,
    }


@router.get("/")
def listar_articulos(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    busqueda: str = Query(None, description="Filtra por nombre, SKU o código de barras"),
    grupo: str = Query(None, description="Filtra por grupo/subfamilia ARTGRUCOD"),
    solo_activos: bool = Query(True, description="Si true, excluye artículos con ARTMOS=1"),
    db: Session = Depends(get_db)
):
    """Lista artículos de la tabla ARTICULO con stock total calculado."""
    query = db.query(models.Articulo)

    if solo_activos:
        query = query.filter(models.Articulo.oculto == 0)
    if grupo:
        query = query.filter(models.Articulo.grupo == grupo)
    if busqueda:
        like = f"%{busqueda}%"
        query = query.filter(
            models.Articulo.nombre.ilike(like) |
            models.Articulo.sku.ilike(like) |
            models.Articulo.barcode.ilike(like) |
            models.Articulo.codigo2.ilike(like)
        )

    total = query.count()
    articulos = query.order_by(models.Articulo.nombre).offset(skip).limit(limit).all()

    # Calcular stock total por artículo (suma de STOCAN en todas las ubicaciones)
    skus = [a.sku for a in articulos]
    stock_map = {}
    if skus:
        stock_rows = (
            db.query(models.Stock.articulo_cod, func.sum(models.Stock.cantidad))
            .filter(models.Stock.articulo_cod.in_(skus))
            .group_by(models.Stock.articulo_cod)
            .all()
        )
        stock_map = {row[0].strip(): (row[1] or 0.0) for row in stock_rows}

    resultado = [_articulo_to_dict(a, stock_map.get(a.sku.strip(), 0.0)) for a in articulos]
    return {"total": total, "productos": resultado}


@router.get("/{sku}")
def obtener_articulo(sku: str, db: Session = Depends(get_db)):
    """Obtiene un artículo por su código ARTCOD."""
    articulo = db.query(models.Articulo).filter(models.Articulo.sku == sku).first()
    if not articulo:
        raise HTTPException(status_code=404, detail=f"Artículo '{sku}' no encontrado")

    cantidad = (
        db.query(func.sum(models.Stock.cantidad))
        .filter(models.Stock.articulo_cod == sku)
        .scalar()
    ) or 0.0

    return _articulo_to_dict(articulo, cantidad)


@router.post("/", status_code=201)
def crear_articulo(item: ArticuloCreate, db: Session = Depends(get_db)):
    """Crea un nuevo artículo en la tabla ARTICULO."""
    existe = db.query(models.Articulo).filter(models.Articulo.sku == item.sku).first()
    if existe:
        raise HTTPException(status_code=400, detail=f"El código '{item.sku}' ya existe")

    nuevo = models.Articulo(
        sku=item.sku.strip().upper(),
        nombre=item.nombre.strip(),
        codigo2=item.codigo2,
        barcode=item.barcode,
        barcode_caja=item.barcode_caja,
        barcode_palet=item.barcode_palet,
        codigo_largo=item.codigo_largo,
        peso_uni=item.peso_uni or 0,
        stock_min=item.stock_min or 0,
        stock_max=item.stock_max or 0,
        precio_coste=item.precio_coste or 0,
        grupo=item.grupo,
        unidad_medida=item.unidad_medida,
        material=item.material,
        color=item.color,
        imagen_url=item.imagen_url,
        oculto=item.oculto or 0,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return _articulo_to_dict(nuevo, 0.0)


@router.put("/{sku}")
def actualizar_articulo(sku: str, datos: ArticuloUpdate, db: Session = Depends(get_db)):
    """Actualiza los campos de un artículo existente."""
    articulo = db.query(models.Articulo).filter(models.Articulo.sku == sku).first()
    if not articulo:
        raise HTTPException(status_code=404, detail=f"Artículo '{sku}' no encontrado")

    for campo, valor in datos.model_dump(exclude_unset=True).items():
        if hasattr(articulo, campo):
            setattr(articulo, campo, valor)

    db.commit()
    db.refresh(articulo)

    cantidad = (
        db.query(func.sum(models.Stock.cantidad))
        .filter(models.Stock.articulo_cod == sku)
        .scalar()
    ) or 0.0

    return _articulo_to_dict(articulo, cantidad)


@router.delete("/{sku}")
def eliminar_articulo(sku: str, db: Session = Depends(get_db)):
    """
    Elimina (o marca como oculto) un artículo.
    En lugar de borrado físico, se pone ARTMOS=1 para mantener la integridad
    referencial con movimientos históricos.
    """
    articulo = db.query(models.Articulo).filter(models.Articulo.sku == sku).first()
    if not articulo:
        raise HTTPException(status_code=404, detail=f"Artículo '{sku}' no encontrado")

    # Borrado lógico: ARTMOS = 1 (ocultar)
    articulo.oculto = 1
    db.commit()
    return {"message": f"Artículo '{sku}' marcado como inactivo"}
