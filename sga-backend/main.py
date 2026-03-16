from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal

import models

from pydantic import BaseModel

app = FastAPI()

# Esto TIENE que ir antes de los endpoints (@app.get)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Esquema para validar los datos que vienen del frontend
class ProductoCreate(BaseModel):
    sku: str
    nombre: str
    stock_minimo: int

@app.get("/productos")
def listar_productos(db: Session = Depends(get_db)):
    productos = db.query(models.Producto).all()
    resultado = []
    
    for p in productos:
        # Buscamos el stock de cada producto manualmente para evitar bucles
        st = db.query(models.Stock).filter(models.Stock.producto_id == p.id).first()
        resultado.append({
            "id": p.id,
            "sku": p.sku,
            "nombre": p.nombre,
            "stock_minimo": p.stock_minimo,
            "cantidad": st.cantidad if st else 0 # Si no hay stock, ponemos 0
        })
    return resultado

@app.post("/productos")
def crear_producto(item: ProductoCreate, db: Session = Depends(get_db)):
    # Comprobar si existe ANTES de hacer el add
    db_prod = db.query(models.Producto).filter(models.Producto.sku == item.sku).first()
    if db_prod:
        raise HTTPException(status_code=400, detail="Ese SKU ya existe en el almacén")
    
    nuevo_prod = models.Producto(sku=item.sku, nombre=item.nombre, stock_minimo=item.stock_minimo)
    db.add(nuevo_prod)
    db.commit()
    return nuevo_prod

@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    # 1. Buscar el producto
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    
    if not producto:
        return {"error": "No existe"}

    try:
        # 2. Borrar primero el stock asociado para que Postgres no se queje
        db.query(models.Stock).filter(models.Stock.producto_id == producto_id).delete()
        
        # 3. Ahora sí, borrar el producto
        db.delete(producto)
        db.commit()
        return {"message": "Borrado con éxito"}
    except Exception as e:
        db.rollback() # Si algo falla, deshacemos el cambio
        print(f"ERROR REAL: {e}") # Esto saldrá en tu terminal
        return {"error": str(e)}


@app.put("/stock/{producto_id}")
def actualizar_cantidad(producto_id: int, cambio: int, db: Session = Depends(get_db)):
    # Buscamos el registro en la tabla stock
    item_stock = db.query(models.Stock).filter(models.Stock.producto_id == producto_id).first()
    
    if not item_stock:
        # Si no existe registro de stock, lo creamos (por ejemplo en la ubicación 1)
        item_stock = models.Stock(producto_id=producto_id, ubicacion_id=1, cantidad=0)
        db.add(item_stock)

    item_stock.cantidad += cambio
    if item_stock.cantidad < 0: item_stock.cantidad = 0
    
    db.commit()
    return {"nueva_cantidad": item_stock.cantidad}


@app.put("/stock/{producto_id}/fijar")
def fijar_cantidad(producto_id: int, cantidad: int, db: Session = Depends(get_db)):
    item_stock = db.query(models.Stock).filter(models.Stock.producto_id == producto_id).first()
    
    if not item_stock:
        item_stock = models.Stock(producto_id=producto_id, ubicacion_id=1, cantidad=0)
        db.add(item_stock)

    item_stock.cantidad = max(0, cantidad) # Evitamos negativos
    db.commit()
    return {"nueva_cantidad": item_stock.cantidad}