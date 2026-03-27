from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal
import models
import schemas
from typing import List
from datetime import datetime

router = APIRouter(prefix="/inventarios", tags=["Inventarios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def _generar_codigo() -> str:
    return f"INV-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"

@router.get("/", response_model=List[schemas.InventarioResponse])
def listar_inventarios(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Inventario).options(joinedload(models.Inventario.lineas)).order_by(models.Inventario.id.desc()).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.InventarioResponse, status_code=201)
def crear_inventario(item: schemas.InventarioCreate, db: Session = Depends(get_db)):
    db_inv = models.Inventario(
        codigo=item.codigo or _generar_codigo(),
        zona_id=item.zona_id,
        responsable_id=item.responsable_id,
        estado='abierto'
    )
    db.add(db_inv)
    db.flush()

    # Si nos pasan líneas manuales (por ejemplo conteos ciegos o pre-carga del backend)
    for linea in item.lineas:
        db_linea = models.InventarioLinea(
            inventario_id=db_inv.id,
            producto_id=linea.producto_id,
            ubicacion_id=linea.ubicacion_id,
            cantidad_sistema=linea.cantidad_sistema,
        )
        db.add(db_linea)
        
    db.commit()
    db.refresh(db_inv)
    return db_inv

@router.put("/{inv_id}/lineas/{linea_id}")
def actualizar_linea(inv_id: int, linea_id: int, cant_fisica: int, db: Session = Depends(get_db)):
    """El operario introduce lo que ha contado realmente"""
    linea = db.query(models.InventarioLinea).filter(models.InventarioLinea.id == linea_id, models.InventarioLinea.inventario_id == inv_id).first()
    if not linea:
        raise HTTPException(404, "Línea no encontrada")
    
    linea.cantidad_fisica = cant_fisica
    linea.diferencia = cant_fisica - linea.cantidad_sistema
    db.commit()
    db.refresh(linea)
    return linea

@router.post("/{inv_id}/cerrar")
def cerrar_inventario(inv_id: int, db: Session = Depends(get_db)):
    """Cierra el inventario y genera movimientos de ajuste (regularización) para cuadrar diferencias"""
    inv = db.query(models.Inventario).options(joinedload(models.Inventario.lineas)).filter(models.Inventario.id == inv_id).first()
    if not inv:
        raise HTTPException(404, "Inventario no encontrado")
    if inv.estado == 'cerrado':
        raise HTTPException(400, "Ya está cerrado")

    try:
        for linea in inv.lineas:
            # Si no se contó nada físico, asumimos que no hubo cambios o que había 0. 
            # Mejor requerir que esté contado.
            if linea.cantidad_fisica is not None and linea.diferencia != 0:
                stock_item = db.query(models.Stock).filter(
                    models.Stock.producto_id == linea.producto_id,
                    models.Stock.ubicacion_id == linea.ubicacion_id
                ).first()
                if not stock_item:
                    stock_item = models.Stock(producto_id=linea.producto_id, ubicacion_id=linea.ubicacion_id, cantidad=0)
                    db.add(stock_item)
                    db.flush()
                
                mov = models.Movimiento(
                    producto_id=linea.producto_id,
                    ubicacion_origen_id=linea.ubicacion_id,
                    ubicacion_destino_id=linea.ubicacion_id,
                    tipo="entrada" if linea.diferencia > 0 else "salida",
                    cantidad=abs(linea.diferencia),
                    cantidad_anterior=stock_item.cantidad,
                    cantidad_nueva=linea.cantidad_fisica,
                    motivo=f"Ajuste inventario {inv.codigo}",
                    fecha=datetime.utcnow()
                )
                stock_item.cantidad = linea.cantidad_fisica
                db.add(mov)

        inv.estado = 'cerrado'
        inv.cerrado_en = datetime.utcnow()
        db.commit()
        return {"mensaje": "Inventario cerrado y stock descuadrado ajustado con éxito."}
    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Error al cerrar: {str(e)}")
