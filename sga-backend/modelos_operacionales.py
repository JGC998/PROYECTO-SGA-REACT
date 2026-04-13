"""
modelos_operacionales.py — Tablas propias del SGA Web para operaciones internas.
Estas tablas viven en el esquema 'sga' y NO son parte de LIN.
Se crean automáticamente al iniciar la aplicación.

Las entidades de negocio (artículos, almacenes, stock) se leen de dbo.*
pero el estado de las operaciones del SGA (recepciones, picking, etc.) se guarda aquí.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import MetaData
from datetime import datetime

# Base separada con esquema sga para las tablas operacionales
sga_metadata = MetaData(schema="sga")
SgaBase = declarative_base(metadata=sga_metadata)


class Recepcion(SgaBase):
    """Recepciones de mercancía registradas en el SGA."""
    __tablename__ = "recepciones"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    codigo          = Column(String(50), unique=True, nullable=False)
    # Referencia al proveedor — ahora es su CLICOD (str), no un int
    proveedor_cod   = Column(String(15), nullable=True)
    estado          = Column(String(20), default='pendiente')  # pendiente, parcial, completada
    fecha_esperada  = Column(DateTime, nullable=True)
    fecha_recepcion = Column(DateTime, nullable=True)
    notas           = Column(Text, nullable=True)
    creado_en       = Column(DateTime, default=datetime.utcnow)

    lineas = relationship("RecepcionLinea", back_populates="recepcion", cascade="all, delete-orphan")


class RecepcionLinea(SgaBase):
    __tablename__ = "recepciones_lineas"

    id                = Column(Integer, primary_key=True, autoincrement=True)
    recepcion_id      = Column(Integer, ForeignKey("sga.recepciones.id"), nullable=False)
    # Artículo — ahora es su SKU (str), no un int
    articulo_cod      = Column(String(10), nullable=False)
    cantidad_esperada = Column(Float, nullable=False)
    cantidad_recibida = Column(Float, default=0)
    estado            = Column(String(20), default='pendiente')
    # Datos de destino
    ubicacion_destino = Column(String(20), nullable=True)
    lote              = Column(String(10), nullable=True, default='')

    recepcion = relationship("Recepcion", back_populates="lineas")


class PickingOrden(SgaBase):
    """Órdenes de picking del SGA web."""
    __tablename__ = "picking_ordenes"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    codigo        = Column(String(50), unique=True, nullable=False)
    # Operario — código de SGAUSUARIO o de sga_usuarios
    operario_cod  = Column(String(10), nullable=True)
    estado        = Column(String(20), default='pendiente')
    prioridad     = Column(Integer, default=1)
    notas         = Column(Text, nullable=True)
    creado_en     = Column(DateTime, default=datetime.utcnow)
    completado_en = Column(DateTime, nullable=True)

    lineas = relationship("PickingLinea", back_populates="picking", cascade="all, delete-orphan")


class PickingLinea(SgaBase):
    __tablename__ = "picking_lineas"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    picking_id          = Column(Integer, ForeignKey("sga.picking_ordenes.id"), nullable=False)
    articulo_cod        = Column(String(10), nullable=False)
    cantidad_solicitada = Column(Float, nullable=False)
    cantidad_recogida   = Column(Float, default=0)
    ubicacion_origen    = Column(String(20), nullable=True)
    estado              = Column(String(20), default='pendiente')

    picking = relationship("PickingOrden", back_populates="lineas")


class Expedicion(SgaBase):
    __tablename__ = "expediciones"

    id                 = Column(Integer, primary_key=True, autoincrement=True)
    codigo             = Column(String(50), unique=True, nullable=False)
    picking_id         = Column(Integer, ForeignKey("sga.picking_ordenes.id"), nullable=True)
    estado             = Column(String(20), default='preparacion')
    agencia_transporte = Column(String(100), nullable=True)
    tracking_number    = Column(String(100), nullable=True)
    creado_en          = Column(DateTime, default=datetime.utcnow)
    fecha_envio        = Column(DateTime, nullable=True)


class Inventario(SgaBase):
    __tablename__ = "inventarios"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    codigo         = Column(String(50), unique=True, nullable=False)
    # Zona/Almacén — ahora es código (str)
    almacen_cod    = Column(String(2), nullable=True)
    responsable_id = Column(Integer, nullable=True)
    estado         = Column(String(20), default='abierto')
    creado_en      = Column(DateTime, default=datetime.utcnow)
    cerrado_en     = Column(DateTime, nullable=True)

    lineas = relationship("InventarioLinea", back_populates="inventario", cascade="all, delete-orphan")


class InventarioLinea(SgaBase):
    __tablename__ = "inventarios_lineas"

    id               = Column(Integer, primary_key=True, autoincrement=True)
    inventario_id    = Column(Integer, ForeignKey("sga.inventarios.id"), nullable=False)
    articulo_cod     = Column(String(10), nullable=False)
    ubicacion_codigo = Column(String(20), nullable=False)
    cantidad_sistema = Column(Float, nullable=False)
    cantidad_fisica  = Column(Float, nullable=True)
    diferencia       = Column(Float, nullable=True)

    inventario = relationship("Inventario", back_populates="lineas")
