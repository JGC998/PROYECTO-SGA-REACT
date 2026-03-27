from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# ── Auth & Usuarios ─────────────────────────────────────────────────────────────

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    rol: Optional[str] = None


class UsuarioBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    email: EmailStr
    rol: str = Field(..., max_length=20)   # 'admin', 'supervisor', 'operario'
    activo: bool = True

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=6)

class UsuarioResponse(UsuarioBase):
    id: int
    ultimo_acceso: Optional[datetime] = None
    creado_en: datetime

    class Config:
        from_attributes = True


# ── Catálogo ──────────────────────────────────────────────────────────────────

class CategoriaBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    descripcion: Optional[str] = Field(None, max_length=300)

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id: int
    class Config:
        from_attributes = True


class ProveedorBase(BaseModel):
    nombre: str = Field(..., max_length=150)
    cif: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    contacto: Optional[str] = Field(None, max_length=100)
    activo: bool = True

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorResponse(ProveedorBase):
    id: int
    class Config:
        from_attributes = True


class ProductoCreate(BaseModel):
    sku: str = Field(..., min_length=1, max_length=50)
    nombre: str = Field(..., min_length=1, max_length=200)
    descripcion: Optional[str] = Field(None, max_length=500)
    categoria_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    unidad_medida: str = Field("ud", max_length=20)
    stock_minimo: int = Field(0, ge=0)
    stock_maximo: Optional[int] = Field(None, ge=0)
    precio_coste: Optional[float] = None
    codigo_barras: Optional[str] = Field(None, max_length=50)
    imagen_url: Optional[str] = Field(None, max_length=500)
    activo: bool = True


class ProductoUpdate(BaseModel):
    sku: Optional[str] = Field(None, min_length=1, max_length=50)
    nombre: Optional[str] = Field(None, min_length=1, max_length=200)
    descripcion: Optional[str] = Field(None, max_length=500)
    categoria_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    unidad_medida: Optional[str] = Field(None, max_length=20)
    stock_minimo: Optional[int] = Field(None, ge=0)
    stock_maximo: Optional[int] = Field(None, ge=0)
    precio_coste: Optional[float] = None
    codigo_barras: Optional[str] = Field(None, max_length=50)
    imagen_url: Optional[str] = Field(None, max_length=500)
    activo: Optional[bool] = None


class ProductoResponse(BaseModel):
    id: int
    sku: str
    nombre: str
    descripcion: Optional[str]
    categoria_id: Optional[int]
    proveedor_id: Optional[int]
    unidad_medida: str
    stock_minimo: int
    stock_maximo: Optional[int]
    precio_coste: Optional[float]
    codigo_barras: Optional[str]
    imagen_url: Optional[str]
    activo: bool
    cantidad: int = 0
    creado_en: datetime

    class Config:
        from_attributes = True


# ── Almacenes y Ubicaciones ───────────────────────────────────────────────────

class AlmacenBase(BaseModel):
    codigo: str = Field(..., max_length=20)
    nombre: str = Field(..., max_length=100)
    direccion: Optional[str] = Field(None, max_length=255)
    activo: bool = True

class AlmacenCreate(AlmacenBase):
    pass

class AlmacenResponse(AlmacenBase):
    id: int
    class Config:
        from_attributes = True


class ZonaBase(BaseModel):
    almacen_id: int
    codigo: str = Field(..., max_length=20)
    nombre: str = Field(..., max_length=100)
    capacidad_max: Optional[int] = None

class ZonaCreate(ZonaBase):
    pass

class ZonaResponse(ZonaBase):
    id: int
    class Config:
        from_attributes = True


class UbicacionCreate(BaseModel):
    zona_id: Optional[int] = None
    codigo: str = Field(..., min_length=1, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=200)
    capacidad_max: Optional[int] = None
    activo: bool = True

class UbicacionResponse(BaseModel):
    id: int
    zona_id: Optional[int]
    codigo: str
    descripcion: Optional[str]
    capacidad_max: Optional[int]
    activo: bool

    class Config:
        from_attributes = True


# ── Movimientos ────────────────────────────────────────────────────────────────

class MovimientoResponse(BaseModel):
    id: int
    codigo: Optional[str]
    producto_id: int
    producto_nombre: Optional[str] = None
    producto_sku: Optional[str] = None
    ubicacion_origen_id: Optional[int]
    ubicacion_destino_id: Optional[int]
    tipo: str
    cantidad: int
    cantidad_anterior: int
    cantidad_nueva: int
    motivo: Optional[str]
    estado: str
    usuario_id: Optional[int]
    fecha: datetime

    class Config:
        from_attributes = True


class MovimientoCreate(BaseModel):
    producto_id: int
    ubicacion_origen_id: Optional[int] = None
    ubicacion_destino_id: Optional[int] = None
    cantidad: int = Field(..., gt=0)
    motivo: Optional[str] = None


# ── Reportes ───────────────────────────────────────────────────────────────────

class ResumenResponse(BaseModel):
    total_productos: int
    productos_bajo_minimo: int
    ultimos_movimientos: List[MovimientoResponse]


# ── Operaciones Core (Fase 3) ────────────────────────────────────────────────

class RecepcionLineaBase(BaseModel):
    producto_id: int
    cantidad_esperada: int
    cantidad_recibida: int = 0
    estado: str = "pendiente"

class RecepcionLineaCreate(RecepcionLineaBase):
    pass

class RecepcionLineaResponse(RecepcionLineaBase):
    id: int
    recepcion_id: int
    class Config:
        from_attributes = True

class RecepcionBase(BaseModel):
    proveedor_id: int
    fecha_esperada: Optional[datetime] = None
    notas: Optional[str] = None

class RecepcionCreate(RecepcionBase):
    codigo: str
    lineas: List[RecepcionLineaCreate] = []

class RecepcionResponse(RecepcionBase):
    id: int
    codigo: str
    estado: str
    fecha_recepcion: Optional[datetime] = None
    creado_en: datetime
    lineas: List[RecepcionLineaResponse] = []
    class Config:
        from_attributes = True

class PickingLineaBase(BaseModel):
    producto_id: int
    cantidad_solicitada: int
    ubicacion_origen_id: Optional[int] = None

class PickingLineaCreate(PickingLineaBase):
    pass

class PickingLineaResponse(PickingLineaBase):
    id: int
    picking_id: int
    cantidad_recogida: int
    estado: str
    class Config:
        from_attributes = True

class PickingOrdenBase(BaseModel):
    operario_id: Optional[int] = None
    prioridad: int = 1
    notas: Optional[str] = None

class PickingOrdenCreate(PickingOrdenBase):
    codigo: str
    lineas: List[PickingLineaCreate] = []

class PickingOrdenResponse(PickingOrdenBase):
    id: int
    codigo: str
    estado: str
    creado_en: datetime
    completado_en: Optional[datetime] = None
    lineas: List[PickingLineaResponse] = []
    class Config:
        from_attributes = True

class ExpedicionBase(BaseModel):
    picking_id: Optional[int] = None
    agencia_transporte: Optional[str] = None
    tracking_number: Optional[str] = None

class ExpedicionCreate(ExpedicionBase):
    codigo: str

class ExpedicionResponse(ExpedicionBase):
    id: int
    codigo: str
    estado: str
    creado_en: datetime
    fecha_envio: Optional[datetime] = None
    class Config:
        from_attributes = True

class InventarioLineaBase(BaseModel):
    producto_id: int
    ubicacion_id: int
    cantidad_sistema: int

class InventarioLineaCreate(InventarioLineaBase):
    pass

class InventarioLineaResponse(InventarioLineaBase):
    id: int
    inventario_id: int
    cantidad_fisica: Optional[int] = None
    diferencia: Optional[int] = None
    class Config:
        from_attributes = True

class InventarioBase(BaseModel):
    zona_id: Optional[int] = None

class InventarioCreate(InventarioBase):
    codigo: str
    responsable_id: int
    lineas: List[InventarioLineaCreate] = []

class InventarioResponse(InventarioBase):
    id: int
    codigo: str
    responsable_id: int
    estado: str
    creado_en: datetime
    cerrado_en: Optional[datetime] = None
    lineas: List[InventarioLineaResponse] = []
    class Config:
        from_attributes = True

