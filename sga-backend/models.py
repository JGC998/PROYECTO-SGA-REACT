from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, DECIMAL
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False)  # 'admin' | 'supervisor' | 'operario'
    activo = Column(Boolean, default=True)
    ultimo_acceso = Column(DateTime, nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)


class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(300), nullable=True)

    productos = relationship("Producto", back_populates="categoria")


class Proveedor(Base):
    __tablename__ = "proveedores"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    cif = Column(String(20), unique=True, nullable=True)
    email = Column(String(150), nullable=True)
    telefono = Column(String(20), nullable=True)
    contacto = Column(String(100), nullable=True)
    activo = Column(Boolean, default=True)

    productos = relationship("Producto", back_populates="proveedor")


class Almacen(Base):
    __tablename__ = "almacenes"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(255), nullable=True)
    activo = Column(Boolean, default=True)

    zonas = relationship("Zona", back_populates="almacen", cascade="all, delete-orphan")


class Zona(Base):
    __tablename__ = "zonas"
    id = Column(Integer, primary_key=True, index=True)
    almacen_id = Column(Integer, ForeignKey("almacenes.id"))
    codigo = Column(String(20), nullable=False)
    nombre = Column(String(100), nullable=False)
    capacidad_max = Column(Integer, nullable=True)

    almacen = relationship("Almacen", back_populates="zonas")
    ubicaciones = relationship("Ubicacion", back_populates="zona", cascade="all, delete-orphan")


class Ubicacion(Base):
    __tablename__ = "ubicaciones"
    id = Column(Integer, primary_key=True, index=True)
    zona_id = Column(Integer, ForeignKey("zonas.id"), nullable=True)
    codigo = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(200), nullable=True)
    capacidad_max = Column(Integer, nullable=True)
    activo = Column(Boolean, default=True)

    zona = relationship("Zona", back_populates="ubicaciones")
    stock = relationship("Stock", back_populates="ubicacion")


class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(String(500), nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"), nullable=True)
    unidad_medida = Column(String(20), default='ud')
    stock_minimo = Column(Integer, default=0, nullable=False)
    stock_maximo = Column(Integer, nullable=True)
    precio_coste = Column(DECIMAL(10, 2), nullable=True)
    codigo_barras = Column(String(50), unique=True, nullable=True)
    imagen_url = Column(String(500), nullable=True)
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime, default=datetime.utcnow)

    categoria = relationship("Categoria", back_populates="productos")
    proveedor = relationship("Proveedor", back_populates="productos")
    stock = relationship("Stock", back_populates="producto",
                         cascade="all, delete-orphan")
    movimientos = relationship("Movimiento", back_populates="producto",
                                cascade="all, delete-orphan")


class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    ubicacion_id = Column(Integer, ForeignKey("ubicaciones.id"), nullable=True)
    cantidad = Column(Integer, default=0, nullable=False)
    lote = Column(String(50), nullable=True)
    fecha_caducidad = Column(DateTime, nullable=True)
    actualizado_en = Column(DateTime, default=datetime.utcnow)

    producto = relationship("Producto", back_populates="stock")
    ubicacion = relationship("Ubicacion", back_populates="stock")


class Movimiento(Base):
    __tablename__ = "movimientos"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), unique=True, nullable=True)  # MOV-0001
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    ubicacion_origen_id = Column(Integer, ForeignKey("ubicaciones.id"), nullable=True)
    ubicacion_destino_id = Column(Integer, ForeignKey("ubicaciones.id"), nullable=True)
    tipo = Column(String(10), nullable=False)           # "entrada" o "salida" o "transferencia"
    cantidad = Column(Integer, nullable=False)
    cantidad_anterior = Column(Integer, nullable=False)
    cantidad_nueva = Column(Integer, nullable=False)
    motivo = Column(String(500), nullable=True)
    estado = Column(String(20), default='completado')
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)

    producto = relationship("Producto", back_populates="movimientos")


class AuditoriaLog(Base):
    __tablename__ = "auditoria_log"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    accion = Column(String(50), nullable=False)
    entidad = Column(String(50), nullable=False)
    entidad_id = Column(Integer, nullable=True)
    datos_antes = Column(String, nullable=True) # Text JSON
    datos_despues = Column(String, nullable=True) # Text JSON
    ip = Column(String(45), nullable=True)
    fecha = Column(DateTime, default=datetime.utcnow)


# ==============================================================================
# FASE 3: OPERACIONES CORE
# ==============================================================================

class Recepcion(Base):
    __tablename__ = "recepciones"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False) # REC-2023-001
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"), nullable=False)
    estado = Column(String(20), default='pendiente') # pendiente, parcial, completada
    fecha_esperada = Column(DateTime, nullable=True)
    fecha_recepcion = Column(DateTime, nullable=True)
    notas = Column(String(500), nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)

    proveedor = relationship("Proveedor")
    lineas = relationship("RecepcionLinea", back_populates="recepcion", cascade="all, delete-orphan")

class RecepcionLinea(Base):
    __tablename__ = "recepciones_lineas"
    id = Column(Integer, primary_key=True, index=True)
    recepcion_id = Column(Integer, ForeignKey("recepciones.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad_esperada = Column(Integer, nullable=False)
    cantidad_recibida = Column(Integer, default=0)
    estado = Column(String(20), default='pendiente') # pendiente, recibida, discrepancia

    recepcion = relationship("Recepcion", back_populates="lineas")
    producto = relationship("Producto")

class PickingOrden(Base):
    __tablename__ = "picking_ordenes"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False) # PIK-2023-001
    operario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    estado = Column(String(20), default='pendiente') # pendiente, en_proceso, completado
    prioridad = Column(Integer, default=1) # 1 normal, 2 alta
    notas = Column(String(500), nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)
    completado_en = Column(DateTime, nullable=True)

    operario = relationship("Usuario")
    lineas = relationship("PickingLinea", back_populates="picking", cascade="all, delete-orphan")

class PickingLinea(Base):
    __tablename__ = "picking_lineas"
    id = Column(Integer, primary_key=True, index=True)
    picking_id = Column(Integer, ForeignKey("picking_ordenes.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad_solicitada = Column(Integer, nullable=False)
    cantidad_recogida = Column(Integer, default=0)
    ubicacion_origen_id = Column(Integer, ForeignKey("ubicaciones.id"), nullable=True)
    estado = Column(String(20), default='pendiente')

    picking = relationship("PickingOrden", back_populates="lineas")
    producto = relationship("Producto")
    ubicacion = relationship("Ubicacion")

class Expedicion(Base):
    __tablename__ = "expediciones"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False) # EXP-2023-001
    picking_id = Column(Integer, ForeignKey("picking_ordenes.id"), nullable=True)
    estado = Column(String(20), default='preparacion') # preparacion, enviada, entregada
    agencia_transporte = Column(String(100), nullable=True)
    tracking_number = Column(String(100), nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow)
    fecha_envio = Column(DateTime, nullable=True)

    picking = relationship("PickingOrden")

class Inventario(Base):
    __tablename__ = "inventarios" # Recuento físico
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False) # INV-2023-001
    zona_id = Column(Integer, ForeignKey("zonas.id"), nullable=True)
    responsable_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    estado = Column(String(20), default='abierto') # abierto, cerrado
    creado_en = Column(DateTime, default=datetime.utcnow)
    cerrado_en = Column(DateTime, nullable=True)

    zona = relationship("Zona")
    responsable = relationship("Usuario")
    lineas = relationship("InventarioLinea", back_populates="inventario", cascade="all, delete-orphan")

class InventarioLinea(Base):
    __tablename__ = "inventarios_lineas"
    id = Column(Integer, primary_key=True, index=True)
    inventario_id = Column(Integer, ForeignKey("inventarios.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    ubicacion_id = Column(Integer, ForeignKey("ubicaciones.id"), nullable=False)
    cantidad_sistema = Column(Integer, nullable=False) # Lo que cree el SGA
    cantidad_fisica = Column(Integer, nullable=True) # Lo que cuenta el operario
    diferencia = Column(Integer, nullable=True) # fisica - sistema

    inventario = relationship("Inventario", back_populates="lineas")
    producto = relationship("Producto")
    ubicacion = relationship("Ubicacion")