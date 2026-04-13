import csv
import os
from sqlalchemy import inspect
from database import engine, Base
import models  # Para asegurar que los modelos se cargan en Base.metadata

def export_db_to_csv(output_dir="database_export"):
    # Crear carpeta si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    inspector = inspect(engine)
    
    # Obtener el esquema, parece que usamos "sga"
    schema = "sga"
    
    try:
        tables = inspector.get_table_names(schema=schema)
    except:
        tables = inspector.get_table_names()

    if not tables:
        print("No se encontraron tablas para exportar.")
        return

    # Exportar cada tabla
    with engine.connect() as connection:
        for table_name in tables:
            print(f"Exportando tabla: {table_name}...")
            # Query para leer todos los datos de la tabla
            query = f'SELECT * FROM [{schema}].[{table_name}]' if schema else f'SELECT * FROM [{table_name}]'
            
            try:
                result = connection.execute(text(query))
                rows = result.fetchall()
                keys = result.keys()

                csv_file_path = os.path.join(output_dir, f"{table_name}.csv")
                with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f, delimiter=';')
                    writer.writerow(keys)  # Escribir cabeceras
                    for row in rows:
                        writer.writerow(row)
                print(f"  -> Guardado en {csv_file_path}")
            except Exception as e:
                print(f"  -> Error al exportar la tabla {table_name}: {e}")

if __name__ == "__main__":
    from sqlalchemy import text
    print("Iniciando exportación de la base de datos a CSV...")
    export_db_to_csv()
    print("Exportación finalizada.")
