import os
import sys
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from auth.jwt import get_password_hash

def init_db():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Crear usuario admin si no existe
    admin = db.query(models.Usuario).filter(models.Usuario.email == "admin@sga.com").first()
    if not admin:
        print("Creando usuario admin@sga.com pwd: admin123")
        admin = models.Usuario(
            nombre="Administrador Sistema",
            email="admin@sga.com",
            password_hash=get_password_hash("admin123"),
            rol="admin",
            activo=True
        )
        db.add(admin)
        db.commit()
    else:
        print("Admin ya existe")

    # Crear usuario supervisor si no existe
    sup = db.query(models.Usuario).filter(models.Usuario.email == "supervisor@sga.com").first()
    if not sup:
        print("Creando usuario supervisor@sga.com pwd: sup123")
        sup = models.Usuario(
            nombre="Supervisor Almacén",
            email="supervisor@sga.com",
            password_hash=get_password_hash("sup123"),
            rol="supervisor",
            activo=True
        )
        db.add(sup)
        db.commit()

    db.close()

if __name__ == "__main__":
    init_db()
