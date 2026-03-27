from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(200), nullable=False)
    stock_minimo = Column(Integer, default=0, nullable=False)

    stock = relationship("Stock", back_populates="producto",
                         cascade="all, delete-orphan", uselist=False)
    movimientos = relationship("Movimiento", back_populates="producto",
                                cascade="all, delete-orphan")


class Ubicacion(Base):
    __tablename__ = "ubicaciones"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(200), nullable=True)

    stock = relationship("Stock", back_populates="ubicacion")


class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    ubicacion_id = Column(Integer, ForeignKey("ubicaciones.id"), nullable=True)
    cantidad = Column(Integer, default=0, nullable=False)

    producto = relationship("Producto", back_populates="stock")
    ubicacion = relationship("Ubicacion", back_populates="stock")


class Movimiento(Base):
    __tablename__ = "movimientos"
    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    tipo = Column(String(10), nullable=False)           # "entrada" o "salida"
    cantidad = Column(Integer, nullable=False)
    cantidad_anterior = Column(Integer, nullable=False)
    cantidad_nueva = Column(Integer, nullable=False)
    motivo = Column(String(500), nullable=True)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)

    producto = relationship("Producto", back_populates="movimientos")