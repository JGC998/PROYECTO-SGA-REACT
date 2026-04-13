"""
Router de Stock — tabla STOCK de LIN (esquema dbo).
PK compuesta: (STOARTCOD, STOUBI, STOLOT).
El stock se consulta siempre en tiempo real desde LIN.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal
import models

router = APIRouter(prefix="/stock", tags=["Stock"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def listar_stock(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    articulo_cod: str = Query(None, description="Filtra por código de artículo (STOARTCOD)"),
    ubicacion: str = Query(None, description="Filtra por código de ubicación (STOUBI)"),
    solo_con_stock: bool = Query(True, description="Si true, muestra solo registros con cantidad > 0"),
    db: Session = Depends(get_db)
):
    """Lista el stock de la tabla STOCK con nombre de artículo."""
    query = db.query(models.Stock)

    if solo_con_stock:
        query = query.filter(models.Stock.cantidad > 0)
    if articulo_cod:
        query = query.filter(models.Stock.articulo_cod == articulo_cod)
    if ubicacion:
        query = query.filter(models.Stock.ubicacion == ubicacion)

    total = query.count()
    stock_rows = query.offset(skip).limit(limit).all()

    # Enriquecer con nombre de artículo
    skus = list({s.articulo_cod.strip() for s in stock_rows})
    articulos_map = {}
    if skus:
        arts = db.query(models.Articulo).filter(models.Articulo.sku.in_(skus)).all()
        articulos_map = {a.sku.strip(): (a.nombre or "").strip() for a in arts}

    resultado = []
    for s in stock_rows:
        cod = (s.articulo_cod or "").strip()
        resultado.append({
            "articulo_cod": cod,
            "articulo_nombre": articulos_map.get(cod, ""),
            "ubicacion": (s.ubicacion or "").strip(),
            "lote": (s.lote or "").strip(),
            "cantidad": s.cantidad or 0.0,
        })

    return {"total": total, "stock": resultado}


@router.get("/resumen")
def resumen_stock(db: Session = Depends(get_db)):
    """
    Stock total por artículo (suma de todas las ubicaciones y lotes).
    Útil para el dashboard y para saber si un artículo está bajo mínimo.
    """
    rows = (
        db.query(
            models.Stock.articulo_cod,
            func.sum(models.Stock.cantidad).label("total")
        )
        .filter(models.Stock.cantidad > 0)
        .group_by(models.Stock.articulo_cod)
        .all()
    )

    # Enriquecer con datos del artículo
    skus = [r[0].strip() for r in rows]
    articulos_map = {}
    if skus:
        arts = db.query(models.Articulo).filter(models.Articulo.sku.in_(skus)).all()
        articulos_map = {a.sku.strip(): a for a in arts}

    resultado = []
    bajo_minimo = 0
    for cod, total in rows:
        cod = cod.strip()
        art = articulos_map.get(cod)
        stock_min = art.stock_min if art else 0
        en_minimo = (total or 0) < (stock_min or 0)
        if en_minimo:
            bajo_minimo += 1
        resultado.append({
            "articulo_cod": cod,
            "articulo_nombre": (art.nombre or "").strip() if art else "",
            "stock_min": stock_min,
            "stock_max": art.stock_max if art else 0,
            "cantidad_total": total or 0.0,
            "bajo_minimo": en_minimo,
        })

    return {
        "total_articulos_con_stock": len(resultado),
        "bajo_minimo": bajo_minimo,
        "detalle": resultado
    }


@router.get("/{articulo_cod}")
def stock_por_articulo(articulo_cod: str, db: Session = Depends(get_db)):
    """Obtiene el stock detallado de un artículo concreto (por ubicación y lote)."""
    articulo = db.query(models.Articulo).filter(models.Articulo.sku == articulo_cod).first()
    if not articulo:
        raise HTTPException(status_code=404, detail=f"Artículo '{articulo_cod}' no encontrado")

    stock_rows = (
        db.query(models.Stock)
        .filter(models.Stock.articulo_cod == articulo_cod, models.Stock.cantidad > 0)
        .all()
    )

    total = sum(s.cantidad or 0 for s in stock_rows)

    return {
        "articulo_cod": articulo_cod,
        "articulo_nombre": (articulo.nombre or "").strip(),
        "stock_min": articulo.stock_min,
        "stock_max": articulo.stock_max,
        "cantidad_total": total,
        "bajo_minimo": total < (articulo.stock_min or 0),
        "detalle": [
            {
                "ubicacion": (s.ubicacion or "").strip(),
                "lote": (s.lote or "").strip(),
                "cantidad": s.cantidad or 0.0,
            }
            for s in stock_rows
        ]
    }
