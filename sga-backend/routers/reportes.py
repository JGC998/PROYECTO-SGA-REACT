"""
Router de Reportes/Dashboard — adaptado a las tablas reales de LIN.
KPIs calculados desde ARTICULO, STOCK y ALBARANCS.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from datetime import datetime, timedelta
from database import SessionLocal
import models

router = APIRouter(prefix="/reportes", tags=["Reportes"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/resumen")
def obtener_resumen_dashboard(db: Session = Depends(get_db)):
    """KPIs generales para el Dashboard."""

    # Total de artículos activos (ARTMOS = 0)
    total_articulos = db.query(models.Articulo).filter(models.Articulo.oculto == 0).count()

    # Stock total (suma de todas las cantidades en STOCK)
    stock_total = db.query(func.sum(models.Stock.cantidad)).scalar() or 0

    # Artículos bajo mínimo:
    # Artículos con stock total < ARTSTOMIN (solo los que tienen stock_min > 0)
    # Subconsulta: stock total por artículo
    stock_por_art = (
        db.query(
            models.Stock.articulo_cod,
            func.sum(models.Stock.cantidad).label("total")
        )
        .group_by(models.Stock.articulo_cod)
        .subquery()
    )
    articulos_bajo_minimo = (
        db.query(models.Articulo)
        .join(stock_por_art, models.Articulo.sku == stock_por_art.c.articulo_cod, isouter=True)
        .filter(
            models.Articulo.stock_min > 0,
            models.Articulo.oculto == 0,
            func.coalesce(stock_por_art.c.total, 0) < models.Articulo.stock_min
        )
        .count()
    )

    # Movimientos de hoy (en ALBARANCS)
    hoy = datetime.utcnow().date()
    movimientos_hoy = (
        db.query(models.MovimientoStock)
        .filter(cast(models.MovimientoStock.fecha, Date) == hoy)
        .count()
    )

    return {
        "productos_activos": total_articulos,
        "unidades_stock": float(stock_total),
        "alertas_stock": articulos_bajo_minimo,
        "movimientos_hoy": movimientos_hoy,
    }


@router.get("/movimientos-por-dia")
def obtener_movimientos_historico(dias: int = 7, db: Session = Depends(get_db)):
    """Datos para la gráfica de barras del Dashboard — movimientos de ALBARANCS agrupados por día."""

    fecha_inicio = datetime.utcnow().date() - timedelta(days=dias - 1)

    resultados = (
        db.query(
            cast(models.MovimientoStock.fecha, Date).label("fecha"),
            models.MovimientoStock.mov,
            func.count().label("total")
        )
        .filter(cast(models.MovimientoStock.fecha, Date) >= fecha_inicio)
        .group_by(
            cast(models.MovimientoStock.fecha, Date),
            models.MovimientoStock.mov
        )
        .all()
    )

    # Inicializar todos los días
    datos_por_dia = {}
    for i in range(dias):
        f = (fecha_inicio + timedelta(days=i)).isoformat()
        datos_por_dia[f] = {"fecha": f, "entradas": 0, "salidas": 0}

    # Tipos de movimiento comunes en LIN: 'E' entrada, 'S' salida
    for row in resultados:
        fecha_str = row.fecha.isoformat()
        mov = (row.mov or "").strip().upper()
        total = row.total

        if fecha_str in datos_por_dia:
            if mov in ("E", "EN"):
                datos_por_dia[fecha_str]["entradas"] += total
            elif mov in ("S", "SA"):
                datos_por_dia[fecha_str]["salidas"] += total

    return list(datos_por_dia.values())


@router.get("/ocupacion-almacenes")
def obtener_ocupacion_almacenes(db: Session = Depends(get_db)):
    """
    Ocupación de stock por Almacén para las barras de progreso del Dashboard.
    Reemplaza el antiguo endpoint de zonas (que no existe en LIN).
    """
    almacenes = db.query(models.Almacen).order_by(models.Almacen.codigo).all()
    resultado = []

    for alm in almacenes:
        # Ubicaciones del almacén
        ubicaciones = (
            db.query(models.Ubicacion)
            .filter(models.Ubicacion.almacen_cod == alm.codigo)
            .all()
        )
        capacidad_total = len(ubicaciones) * 100  # Estimación si no hay capacidad_max

        # Stock en estas ubicaciones
        codigos_ubi = [(u.codigo or "").strip() for u in ubicaciones if u.codigo]
        stock_alm = 0
        if codigos_ubi:
            stock_alm = (
                db.query(func.sum(models.Stock.cantidad))
                .filter(models.Stock.ubicacion.in_(codigos_ubi), models.Stock.cantidad > 0)
                .scalar()
            ) or 0

        porcentaje = round((stock_alm / capacidad_total) * 100, 2) if capacidad_total > 0 else 0

        resultado.append({
            "zona": f"{alm.codigo} - {(alm.nombre or '').strip()}",
            "almacen_cod": alm.codigo,
            "num_ubicaciones": len(ubicaciones),
            "stock_total": float(stock_alm),
            "porcentaje": min(100, porcentaje)
        })

    return resultado


@router.get("/articulos-bajo-minimo")
def articulos_bajo_minimo(limit: int = 20, db: Session = Depends(get_db)):
    """Lista de artículos con stock por debajo del mínimo configurado (ARTSTOMIN)."""
    stock_por_art = (
        db.query(
            models.Stock.articulo_cod,
            func.sum(models.Stock.cantidad).label("total")
        )
        .group_by(models.Stock.articulo_cod)
        .subquery()
    )

    filas = (
        db.query(models.Articulo, func.coalesce(stock_por_art.c.total, 0).label("cantidad_actual"))
        .join(stock_por_art, models.Articulo.sku == stock_por_art.c.articulo_cod, isouter=True)
        .filter(
            models.Articulo.stock_min > 0,
            models.Articulo.oculto == 0,
            func.coalesce(stock_por_art.c.total, 0) < models.Articulo.stock_min
        )
        .order_by(models.Articulo.sku)
        .limit(limit)
        .all()
    )

    return [
        {
            "sku": art.sku,
            "nombre": (art.nombre or "").strip(),
            "stock_min": art.stock_min,
            "stock_actual": float(cantidad),
            "deficit": float(art.stock_min - cantidad)
        }
        for art, cantidad in filas
    ]
