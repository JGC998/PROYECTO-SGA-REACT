from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal
import models
from schemas import ProductoCreate, ProductoUpdate

router = APIRouter(prefix="/productos", tags=["Productos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def listar_productos(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    total = db.query(models.Producto).count()
    productos = (
        db.query(models.Producto)
        .options(joinedload(models.Producto.stock))
        .offset(skip)
        .limit(limit)
        .all()
    )
    resultado = []
    for p in productos:
        resultado.append({
            "id": p.id,
            "sku": p.sku,
            "nombre": p.nombre,
            "stock_minimo": p.stock_minimo,
            "cantidad": p.stock.cantidad if p.stock else 0,
        })
    return {"total": total, "productos": resultado}


@router.post("/", status_code=201)
def crear_producto(item: ProductoCreate, db: Session = Depends(get_db)):
    db_prod = db.query(models.Producto).filter(models.Producto.sku == item.sku).first()
    if db_prod:
        raise HTTPException(status_code=400, detail="Ese SKU ya existe en el almacén")

    nuevo_prod = models.Producto(
        sku=item.sku.strip(),
        nombre=item.nombre.strip(),
        stock_minimo=item.stock_minimo,
    )
    db.add(nuevo_prod)
    db.commit()
    db.refresh(nuevo_prod)
    return {
        "id": nuevo_prod.id,
        "sku": nuevo_prod.sku,
        "nombre": nuevo_prod.nombre,
        "stock_minimo": nuevo_prod.stock_minimo,
        "cantidad": 0,
    }


@router.put("/{producto_id}")
def actualizar_producto(producto_id: int, datos: ProductoUpdate, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Verificar SKU duplicado si se está cambiando
    if datos.sku and datos.sku != producto.sku:
        existe = db.query(models.Producto).filter(models.Producto.sku == datos.sku).first()
        if existe:
            raise HTTPException(status_code=400, detail="Ese SKU ya está en uso")

    for campo, valor in datos.model_dump(exclude_unset=True).items():
        if valor is not None:
            setattr(producto, campo, valor)

    db.commit()
    db.refresh(producto)
    cantidad = producto.stock.cantidad if producto.stock else 0
    return {
        "id": producto.id,
        "sku": producto.sku,
        "nombre": producto.nombre,
        "stock_minimo": producto.stock_minimo,
        "cantidad": cantidad,
    }


@router.delete("/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    try:
        db.delete(producto)   # La cascada borra stock y movimientos automáticamente
        db.commit()
        return {"message": "Borrado con éxito"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
