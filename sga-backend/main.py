from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from dotenv import load_dotenv
import os

from database import engine
import models
import modelos_operacionales
from routers import (
    productos, stock, movimientos, ubicaciones, reportes,
    auth, usuarios, categorias, proveedores, almacenes, recepciones,
    picking, expediciones, inventarios, auditoria
)

load_dotenv()

# ─── Crear tablas propias del SGA (solo las que viven en el esquema 'sga') ────
# Las tablas de LIN (dbo.*) ya existen y NO se tocan.
try:
    with engine.connect() as conn:
        conn.execute(
            text("IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'sga') EXEC('CREATE SCHEMA sga')")
        )
        conn.commit()
except Exception:
    pass  # El esquema ya existe

# Crear tabla de usuarios web y auditoría
models.Usuario.__table__.create(bind=engine, checkfirst=True)
models.AuditoriaLog.__table__.create(bind=engine, checkfirst=True)

# Crear tablas operacionales del SGA (recepciones, picking, etc.)
modelos_operacionales.SgaBase.metadata.create_all(bind=engine)

app = FastAPI(
    title="SGA API",
    description="Sistema de Gestión de Almacén — API REST sobre base de datos LIN",
    version="2.0.0",
)

# CORS restringido a las origins definidas en .env
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar todos los routers
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(categorias.router)
app.include_router(proveedores.router)
app.include_router(almacenes.router)
app.include_router(productos.router)
app.include_router(stock.router)
app.include_router(movimientos.router)
app.include_router(ubicaciones.router)
app.include_router(reportes.router)
app.include_router(recepciones.router)
app.include_router(picking.router)
app.include_router(expediciones.router)
app.include_router(inventarios.router)
app.include_router(auditoria.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "SGA API v2.0 funcionando correctamente",
        "docs": "/docs",
        "db": "LIN (SQL Server 2022)"
    }