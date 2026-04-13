from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Union
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


# ── Artículos (antes: Productos) ──────────────────────────────────────────────
# La PK ahora es 'sku' (str, ARTCOD), no un int autoincremental.

class ArticuloCreate(BaseModel):
    sku: str = Field(..., min_length=1, max_length=10, description="Código ARTCOD de la tabla ARTICULO")
    nombre: str = Field(..., min_length=1, max_length=50)
    codigo2: Optional[str] = Field(None, max_length=30)
    barcode: Optional[str] = Field(None, max_length=30)
    barcode_caja: Optional[str] = Field(None, max_length=30)
    barcode_palet: Optional[str] = Field(None, max_length=14)
    codigo_largo: Optional[str] = Field(None, max_length=50)
    peso_uni: Optional[float] = Field(0.0, ge=0)
    stock_min: Optional[float] = Field(0.0, ge=0)
    stock_max: Optional[float] = Field(0.0, ge=0)
    precio_coste: Optional[float] = Field(None, ge=0)
    grupo: Optional[str] = Field(None, max_length=5)
    unidad_medida: Optional[str] = Field(None, max_length=20)
    material: Optional[str] = Field(None, max_length=20)
    color: Optional[str] = Field(None, max_length=20)
    imagen_url: Optional[str] = Field(None, max_length=255)
    oculto: Optional[int] = Field(0)

# Para compatibilidad con código frontend que usa ProductoCreate
ProductoCreate = ArticuloCreate


class ArticuloUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=50)
    codigo2: Optional[str] = Field(None, max_length=30)
    barcode: Optional[str] = Field(None, max_length=30)
    barcode_caja: Optional[str] = Field(None, max_length=30)
    barcode_palet: Optional[str] = Field(None, max_length=14)
    codigo_largo: Optional[str] = Field(None, max_length=50)
    peso_uni: Optional[float] = Field(None, ge=0)
    stock_min: Optional[float] = Field(None, ge=0)
    stock_max: Optional[float] = Field(None, ge=0)
    precio_coste: Optional[float] = Field(None, ge=0)
    grupo: Optional[str] = Field(None, max_length=5)
    unidad_medida: Optional[str] = Field(None, max_length=20)
    material: Optional[str] = Field(None, max_length=20)
    color: Optional[str] = Field(None, max_length=20)
    imagen_url: Optional[str] = Field(None, max_length=255)
    oculto: Optional[int] = None

ProductoUpdate = ArticuloUpdate


class ArticuloResponse(BaseModel):
    sku: str               # Antes: id: int — ahora es el código ARTCOD
    id: str                # Alias de sku para compatibilidad frontend
    nombre: Optional[str]
    codigo2: Optional[str]
    barcode: Optional[str]
    barcode_caja: Optional[str]
    barcode_palet: Optional[str]
    codigo_largo: Optional[str]
    peso_uni: Optional[float]
    stock_min: Optional[float]
    stock_max: Optional[float]
    precio_coste: Optional[float]
    grupo: Optional[str]
    unidad_medida: Optional[str]
    material: Optional[str]
    color: Optional[str]
    imagen_url: Optional[str]
    activo: bool
    cantidad: float = 0.0  # Suma de STOCAN desde STOCK

    class Config:
        from_attributes = True

ProductoResponse = ArticuloResponse


# ── Almacenes ─────────────────────────────────────────────────────────────────
# La PK ahora es 'codigo' (str, ALMCOD de 2 chars), no un int.

class AlmacenCreate(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=2, description="Código ALMCOD")
    nombre: str = Field(..., min_length=1, max_length=50)

class AlmacenResponse(BaseModel):
    codigo: str
    id: str          # Alias de codigo para compatibilidad frontend
    nombre: Optional[str]
    activo: bool = True

    class Config:
        from_attributes = True


# ── Ubicaciones ───────────────────────────────────────────────────────────────
# La PK ahora es 'id' (float, UBICON — numérico secuencial de LIN).

class UbicacionCreate(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=20, description="Código UBICODUBI")
    nombre: Optional[str] = Field(None, max_length=50)
    almacen_cod: Optional[str] = Field(None, max_length=2)
    alto: Optional[float] = None
    ancho: Optional[float] = None
    num_palets: Optional[int] = Field(1, ge=1)

class UbicacionResponse(BaseModel):
    id: float             # UBICON (float)
    codigo: str
    descripcion: Optional[str]    # alias de nombre
    nombre: Optional[str]
    almacen_cod: Optional[str]
    activo: bool = True
    libre: Optional[int]

    class Config:
        from_attributes = True


# ── Proveedores / Clientes ────────────────────────────────────────────────────
# La PK compuesta (CLICOD + CLICENCOD) — exponemos CLICOD como identificador.

class ProveedorCreate(BaseModel):
    cod: str = Field(..., min_length=1, max_length=15, description="CLICOD")
    cen_cod: str = Field(default="", max_length=4, description="CLICENCOD")
    razon: Optional[str] = Field(None, max_length=50)
    nombre: str = Field(..., min_length=1, max_length=50)
    nif: Optional[str] = Field(None, max_length=15)
    telefono: Optional[str] = Field(None, max_length=40)
    email: Optional[str] = Field(None, max_length=50)
    contacto: Optional[str] = Field(None, max_length=50)
    direccion: Optional[str] = Field(None, max_length=100)
    ciudad: Optional[str] = Field(None, max_length=30)
    provincia: Optional[str] = Field(None, max_length=15)
    cp: Optional[str] = Field(None, max_length=10)

class ProveedorResponse(BaseModel):
    cod: str
    id: str          # Alias de cod
    cen_cod: Optional[str]
    razon: Optional[str]
    nombre: Optional[str]
    nif: Optional[str]
    cif: Optional[str]   # alias de nif
    telefono: Optional[str]
    email: Optional[str]
    contacto: Optional[str]
    direccion: Optional[str]
    ciudad: Optional[str]
    provincia: Optional[str]
    cp: Optional[str]
    activo: bool = True

    class Config:
        from_attributes = True


class ClienteResponse(BaseModel):
    cod: str
    id: str
    cen_cod: Optional[str]
    razon: Optional[str]
    nombre: Optional[str]
    nif: Optional[str]
    telefono: Optional[str]
    email: Optional[str]
    contacto: Optional[str]
    ciudad: Optional[str]

    class Config:
        from_attributes = True


# ── Stock ─────────────────────────────────────────────────────────────────────

class StockResponse(BaseModel):
    articulo_cod: str
    ubicacion: str
    lote: str
    cantidad: Optional[float]

    class Config:
        from_attributes = True


# ── Movimientos ────────────────────────────────────────────────────────────────
# Basados en la tabla ALBARANCS de LIN.

class MovimientoResponse(BaseModel):
    serie: str
    ejercicio: str
    numero: float
    mov: str
    fecha: Optional[datetime]
    articulo_cod: Optional[str]
    cantidad: Optional[float]
    lote: Optional[str]
    ubicacion: Optional[str]
    tipo_mov: Optional[str]
    almacen_cod: Optional[str]
    cliente_cod: Optional[str]
    cliente_nom: Optional[str]
    num_alb: Optional[str]

    class Config:
        from_attributes = True


# ── Categorías / Subfamilias ──────────────────────────────────────────────────
# En LIN se llaman SUBFAMILIA.

class CategoriaCreate(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=5, description="SUBFAMCOD")
    nombre: str = Field(..., min_length=1, max_length=50)

class CategoriaResponse(BaseModel):
    codigo: str
    id: str          # Alias de codigo
    nombre: Optional[str]

    class Config:
        from_attributes = True


# ── Schemas de compatibilidad (operaciones Fase 3) ────────────────────────────
# Picking, Recepciones, Expediciones e Inventarios:
# Estas operaciones son nuevas — por ahora mantienen IDs int propios ya que
# se gestionarán en tablas propias del SGA si no existen sus equivalentes en LIN.

class PickingLineaCreate(BaseModel):
    articulo_cod: str = Field(..., description="Código de artículo (ARTCOD)")
    cantidad_solicitada: float
    ubicacion_origen: Optional[str] = None

class PickingOrdenCreate(BaseModel):
    operario_cod: Optional[str] = None
    prioridad: int = 1
    notas: Optional[str] = None
    lineas: List[PickingLineaCreate] = []

class PickingResponse(BaseModel):
    id: float
    operario_cod: Optional[str]
    fecha_ini: Optional[datetime]
    fecha_fin: Optional[datetime]

    class Config:
        from_attributes = True


# ── Reportes ───────────────────────────────────────────────────────────────────

class ResumenResponse(BaseModel):
    total_articulos: int
    articulos_bajo_minimo: int
    ultimos_movimientos: List[MovimientoResponse]
