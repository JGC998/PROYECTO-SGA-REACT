from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal
import models
import schemas
from typing import List
from datetime import datetime

router = APIRouter(prefix="/recepciones", tags=["Recepciones"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def _generar_codigo() -> str:
    # Genera un codigo único basado en tiempo, ej: REC-20231024-1234
    return f"REC-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"

@router.get("/", response_model=List[schemas.RecepcionResponse])
def listar_recepciones(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Recepcion).options(joinedload(models.Recepcion.lineas)).order_by(models.Recepcion.id.desc()).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.RecepcionResponse, status_code=201)
def crear_recepcion(item: schemas.RecepcionCreate, db: Session = Depends(get_db)):
    # Crear cabecera
    db_rec = models.Recepcion(
        codigo=item.codigo or _generar_codigo(),
        proveedor_id=item.proveedor_id,
        fecha_esperada=item.fecha_esperada,
        notas=item.notas,
        estado='pendiente'
    )
    db.add(db_rec)
    db.flush() # Para obtener db_rec.id

    # Crear lineas
    for linea in item.lineas:
        db_linea = models.RecepcionLinea(
            recepcion_id=db_rec.id,
            producto_id=linea.producto_id,
            cantidad_esperada=linea.cantidad_esperada,
            cantidad_recibida=linea.cantidad_recibida,
            estado=linea.estado
        )
        db.add(db_linea)
        
    db.commit()
    db.refresh(db_rec)
    return db_rec

@router.put("/{recepcion_id}/confirmar")
def confirmar_recepcion(recepcion_id: int, db: Session = Depends(get_db)):
    """Confirma la recepción, cerrando sus líneas e incrementando el stock."""
    db_rec = db.query(models.Recepcion).options(joinedload(models.Recepcion.lineas)).filter(models.Recepcion.id == recepcion_id).first()
    if not db_rec:
        raise HTTPException(404, "Recepción no encontrada")
    if db_rec.estado == 'completada':
        raise HTTPException(400, "La recepción ya está completada")

    try:
        for linea in db_rec.lineas:
            # Asumimos que la recepcion ya fue editada con las cantidades correctas recibidas
            # Incrementamos stock
            stock_item = db.query(models.Stock).filter(models.Stock.producto_id == linea.producto_id).first()
            if not stock_item:
                stock_item = models.Stock(producto_id=linea.producto_id, cantidad=0)
                db.add(stock_item)
                db.flush()
            
            # Movimiento "entrada"
            cantidad_anterior = stock_item.cantidad
            stock_item.cantidad += linea.cantidad_recibida
            
            if linea.cantidad_recibida > 0:
                mov = models.Movimiento(
                    producto_id=linea.producto_id,
                    tipo="entrada",
                    cantidad=linea.cantidad_recibida,
                    cantidad_anterior=cantidad_anterior,
                    cantidad_nueva=stock_item.cantidad,
                    motivo=f"Entrada por recepción {db_rec.codigo}",
                    fecha=datetime.utcnow()
                )
                db.add(mov)

            # Actualizamos estado de la línea
            if linea.cantidad_recibida == linea.cantidad_esperada:
                linea.estado = 'recibida'
            elif linea.cantidad_recibida == 0:
                linea.estado = 'pendiente'
            else:
                linea.estado = 'discrepancia'

        # Actualizar estado de la cabecera
        db_rec.estado = 'completada'
        db_rec.fecha_recepcion = datetime.utcnow()
        db.commit()
        return {"mensaje": "Recepción procesada", "recepcion_id": db_rec.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Error confirmando recepción: {str(e)}")

@router.put("/{recepcion_id}/lineas/{linea_id}")
def actualizar_linea(recepcion_id: int, linea_id: int, cant_recibida: int, db: Session = Depends(get_db)):
    linea = db.query(models.RecepcionLinea).filter(models.RecepcionLinea.id == linea_id, models.RecepcionLinea.recepcion_id == recepcion_id).first()
    if not linea:
        raise HTTPException(404, "Línea no encontrada")
    
    linea.cantidad_recibida = cant_recibida
    db.commit()
    db.refresh(linea)
    return linea
