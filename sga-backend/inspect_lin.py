import os
from sqlalchemy import create_engine, inspect

# Create engine for LIN db
SQLALCHEMY_DATABASE_URL = "mssql+pymssql://SA:SuperSecurePassword123!@localhost:1433/LIN"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

inspector = inspect(engine)
print("--- Schemas ---")
schemas = inspector.get_schema_names()
print(schemas)

for schema in schemas:
    try:
        tables = inspector.get_table_names(schema=schema)
        if tables:
            print(f"\n--- Tables in schema '{schema}' ---")
            print(tables[:20]) # Print first 20 tables
            if len(tables) > 20:
                print(f"... and {len(tables) - 20} more.")
    except Exception as e:
        print(f"Could not read tables for schema {schema}: {e}")
