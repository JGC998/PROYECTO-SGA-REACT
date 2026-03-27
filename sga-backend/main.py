from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from database import engine
import models
from routers import (
    productos, stock, movimientos, ubicaciones, reportes,
    auth, usuarios, categorias, proveedores, almacenes, recepciones,
    picking, expediciones, inventarios, auditoria
)

load_dotenv()

# Crear todas las tablas si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SGA API",
    description="Sistema de Gestión de Almacén — API REST",
    version="1.0.0",
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
    return {"message": "SGA API funcionando correctamente", "docs": "/docs"}