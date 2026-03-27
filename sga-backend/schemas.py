from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ── Productos ──────────────────────────────────────────────────────────────────

class ProductoCreate(BaseModel):
    sku: str = Field(..., min_length=1, max_length=50)
    nombre: str = Field(..., min_length=1, max_length=200)
    stock_minimo: int = Field(..., ge=0)


class ProductoUpdate(BaseModel):
    sku: Optional[str] = Field(None, min_length=1, max_length=50)
    nombre: Optional[str] = Field(None, min_length=1, max_length=200)
    stock_minimo: Optional[int] = Field(None, ge=0)


class ProductoResponse(BaseModel):
    id: int
    sku: str
    nombre: str
    stock_minimo: int
    cantidad: int = 0

    class Config:
        from_attributes = True


# ── Ubicaciones ────────────────────────────────────────────────────────────────

class UbicacionCreate(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=200)


class UbicacionResponse(BaseModel):
    id: int
    codigo: str
    descripcion: Optional[str]

    class Config:
        from_attributes = True


# ── Movimientos ────────────────────────────────────────────────────────────────

class MovimientoResponse(BaseModel):
    id: int
    producto_id: int
    producto_nombre: Optional[str] = None
    producto_sku: Optional[str] = None
    tipo: str
    cantidad: int
    cantidad_anterior: int
    cantidad_nueva: int
    motivo: Optional[str]
    fecha: datetime

    class Config:
        from_attributes = True


# ── Reportes ───────────────────────────────────────────────────────────────────

class ResumenResponse(BaseModel):
    total_productos: int
    productos_bajo_minimo: int
    ultimos_movimientos: list[MovimientoResponse]
