from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True)
    nombre = Column(String)
    stock_minimo = Column(Integer)

class Ubicacion(Base):
    __tablename__ = "ubicaciones"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True)
    descripcion = Column(String)

class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    ubicacion_id = Column(Integer, ForeignKey("ubicaciones.id"))
    cantidad = Column(Integer, default=0)