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
def listar_productos(skip: int = 0, limit: int = 50, 
                     categoria_id: int = None, proveedor_id: int = None, activo: bool = None,
                     db: Session = Depends(get_db)):
    query = db.query(models.Producto).options(joinedload(models.Producto.stock))
    
    if categoria_id is not None:
        query = query.filter(models.Producto.categoria_id == categoria_id)
    if proveedor_id is not None:
        query = query.filter(models.Producto.proveedor_id == proveedor_id)
    if activo is not None:
        query = query.filter(models.Producto.activo == activo)
        
    total = query.count()
    productos = query.offset(skip).limit(limit).all()
    
    resultado = []
    for p in productos:
        resultado.append({
            "id": p.id,
            "sku": p.sku,
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "categoria_id": p.categoria_id,
            "proveedor_id": p.proveedor_id,
            "unidad_medida": p.unidad_medida,
            "stock_minimo": p.stock_minimo,
            "stock_maximo": p.stock_maximo,
            "precio_coste": float(p.precio_coste) if p.precio_coste else None,
            "codigo_barras": p.codigo_barras,
            "imagen_url": p.imagen_url,
            "activo": p.activo,
            "cantidad": p.stock.cantidad if p.stock else 0,
            "creado_en": p.creado_en.isoformat() if p.creado_en else None
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
        descripcion=item.descripcion,
        categoria_id=item.categoria_id,
        proveedor_id=item.proveedor_id,
        unidad_medida=item.unidad_medida,
        stock_minimo=item.stock_minimo,
        stock_maximo=item.stock_maximo,
        precio_coste=item.precio_coste,
        codigo_barras=item.codigo_barras,
        imagen_url=item.imagen_url,
        activo=item.activo
    )
    db.add(nuevo_prod)
    db.commit()
    db.refresh(nuevo_prod)
    
    return {
        "id": nuevo_prod.id,
        "sku": nuevo_prod.sku,
        "nombre": nuevo_prod.nombre,
        "descripcion": nuevo_prod.descripcion,
        "categoria_id": nuevo_prod.categoria_id,
        "proveedor_id": nuevo_prod.proveedor_id,
        "unidad_medida": nuevo_prod.unidad_medida,
        "stock_minimo": nuevo_prod.stock_minimo,
        "stock_maximo": nuevo_prod.stock_maximo,
        "precio_coste": float(nuevo_prod.precio_coste) if nuevo_prod.precio_coste else None,
        "codigo_barras": nuevo_prod.codigo_barras,
        "imagen_url": nuevo_prod.imagen_url,
        "activo": nuevo_prod.activo,
        "cantidad": 0,
        "creado_en": nuevo_prod.creado_en.isoformat() if nuevo_prod.creado_en else None
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
        "descripcion": producto.descripcion,
        "categoria_id": producto.categoria_id,
        "proveedor_id": producto.proveedor_id,
        "unidad_medida": producto.unidad_medida,
        "stock_minimo": producto.stock_minimo,
        "stock_maximo": producto.stock_maximo,
        "precio_coste": float(producto.precio_coste) if producto.precio_coste else None,
        "codigo_barras": producto.codigo_barras,
        "imagen_url": producto.imagen_url,
        "activo": producto.activo,
        "cantidad": cantidad,
        "creado_en": producto.creado_en.isoformat() if producto.creado_en else None
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
