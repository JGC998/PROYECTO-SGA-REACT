# PROYECTO-SGA-REACT

Sistema de Gestión de Almacén desarrollado como proyecto de prácticas. Permite el control de inventario, gestión de stock en tiempo real y alertas de reposición.
🚀 Tecnologías Utilizadas
Backend

    Lenguaje: Python 3.14+

    Framework: FastAPI

    ORM: SQLAlchemy

    Base de datos: PostgreSQL

    Servidor: Uvicorn

Frontend

    Framework: React + Vite

    Comunicación: Axios

    Estilos: CSS3 (Custom)

    Notificaciones: React Hot Toast

🛠️ Instalación y Puesta en Marcha
1. Servidor (Backend)
Bash

cd sga-backend
python -m venv venv
source venv/bin/activate  # En Fedora/Linux
pip install -r requirements.txt
python -m uvicorn main:app --reload

2. Cliente (Frontend)
Bash

cd sga-frontend
npm install
npm run dev

📋 Funcionalidades Actuales

    ✅ CRUD Completo: Creación, lectura y borrado de productos.

    ✅ Control de Stock: Ajuste mediante botones (+/-) y edición manual directa en tabla.

    ✅ Buscador: Filtrado en tiempo real por nombre o SKU.

    ✅ Alertas Visuales: Resaltado automático de productos bajo el stock mínimo.

    ✅ Validación de Datos: Prevención de duplicados de SKU y manejo de errores con Toasts.

📂 Estructura del Proyecto

    /sga-backend: Lógica de negocio, modelos de base de datos y API.

    /sga-frontend: Interfaz de usuario modularizada por dominios (Inicio, Productos, Comunes).