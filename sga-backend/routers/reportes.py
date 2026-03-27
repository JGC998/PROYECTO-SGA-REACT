from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
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
    
    total_productos = db.query(models.Producto).filter(models.Producto.activo == True).count()
    
    stock_total = db.query(func.sum(models.Stock.cantidad)).scalar() or 0
    
    # Bajo mínimo
    productos_bajo_minimo = db.query(models.Producto).join(models.Stock).filter(
        models.Stock.cantidad < models.Producto.stock_minimo,
        models.Producto.activo == True
    ).count()
    
    # Movimientos de hoy
    hoy = datetime.utcnow().date()
    movimientos_hoy = db.query(models.Movimiento).filter(
        func.date(models.Movimiento.fecha) == hoy
    ).count()

    return {
        "productos_activos": total_productos,
        "unidades_stock": stock_total,
        "alertas_stock": productos_bajo_minimo,
        "movimientos_hoy": movimientos_hoy,
    }

@router.get("/movimientos-por-dia")
def obtener_movimientos_historico(dias: int = 7, db: Session = Depends(get_db)):
    """Datos para la gráfica de barras del Dashboard."""
    
    fecha_inicio = datetime.utcnow().date() - timedelta(days=dias-1)
    
    # Agrupar por fecha y tipo
    resultados = db.query(
        func.date(models.Movimiento.fecha).label('fecha'),
        models.Movimiento.tipo,
        func.count(models.Movimiento.id).label('total')
    ).filter(
        func.date(models.Movimiento.fecha) >= fecha_inicio
    ).group_by(
        func.date(models.Movimiento.fecha),
        models.Movimiento.tipo
    ).all()

    # Formatear datos para recharts
    datos_por_dia = {}
    
    # Inicializar todos los días a 0
    for i in range(dias):
        f = (fecha_inicio + timedelta(days=i)).isoformat()
        datos_por_dia[f] = {"fecha": f, "entradas": 0, "salidas": 0}

    for row in resultados:
        fecha_str = row.fecha.isoformat()
        tipo = row.tipo # "entrada" o "salida"
        total = row.total
        
        if fecha_str in datos_por_dia:
            if tipo == "entrada":
                datos_por_dia[fecha_str]["entradas"] += total
            else:
                datos_por_dia[fecha_str]["salidas"] += total

    # Devolver array ordenado
    return list(datos_por_dia.values())


@router.get("/ocupacion-zonas")
def obtener_ocupacion_zonas(db: Session = Depends(get_db)):
    """Ocupación de stock por Zona para las barras de progreso inferiores."""
    
    zonas = db.query(models.Zona).filter(models.Zona.activo == True).all()
    resultado = []
    
    for z in zonas:
        # Calcular capacidad total de la zona (sumando de sus ubicaciones)
        ubicaciones = db.query(models.Ubicacion).filter(models.Ubicacion.zona_id == z.id).all()
        capacidad_total = sum((u.capacidad_max or 100) for u in ubicaciones)
        
        # Calcular items almacenados en esta zona
        ubicaciones_ids = [u.id for u in ubicaciones]
        stock_zona = 0
        if ubicaciones_ids:
            stock_zona = db.query(func.sum(models.Stock.cantidad)).filter(
                models.Stock.ubicacion_id.in_(ubicaciones_ids)
            ).scalar() or 0
        
        porcentaje = round((stock_zona / capacidad_total) * 100, 2) if capacidad_total > 0 else 0
        
        resultado.append({
            "zona": z.nombre,
            "porcentaje": min(100, porcentaje)
        })
        
    return resultado
