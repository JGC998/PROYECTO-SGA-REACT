import os
from sqlalchemy import create_engine, MetaData, Table, inspect, text
from database import SessionLocal, engine
from models import Producto
from dotenv import load_dotenv

load_dotenv()

def migrate_sample_products():
    print("Iniciando migración de prueba desde dbo.ARTICULO hasta sga.productos...")
    db = SessionLocal()
    
    try:
        # Obtenemos los 10 primeros artículos de la base de datos vieja (dbo)
        query = text("""
            SELECT TOP 10 
                ARTCOD, 
                ARTNOM, 
                ARTBARCOD
            FROM dbo.ARTICULO
            WHERE ARTNOM IS NOT NULL AND RTRIM(LTRIM(ARTNOM)) <> ''
        """)
        
        result = db.execute(query).fetchall()
        
        migrados = 0
        for row in result:
            sku = str(row.ARTCOD).strip()
            nombre = str(row.ARTNOM).strip()
            barcode = str(row.ARTBARCOD).strip() if row.ARTBARCOD else None
            if not barcode or barcode == '':
                barcode = f"GEN-{sku}"
            
            # Comprobar si ya existe
            existe = db.query(Producto).filter(Producto.sku == sku).first()
            if not existe:
                nuevo_prod = Producto(
                    sku=sku,
                    nombre=nombre,
                    descripcion=f"Migrado desde DBO",
                    codigo_barras=barcode,
                    stock_minimo=0
                )
                db.add(nuevo_prod)
                migrados += 1
                
        db.commit()
        print(f"Migrados {migrados} productos exitosamente!")
        
    except Exception as e:
        print(f"Error durante la migración: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate_sample_products()
