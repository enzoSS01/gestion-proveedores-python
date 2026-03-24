#mod1_conectar.py
import mariadb
import os
from dotenv import load_dotenv

load_dotenv() # Carga las variables del archivo .env

def conectar():
    try:
        conexion = mariadb.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            database="control_proveedores"
        )
        return conexion
    except mariadb.Error as e:
        print(f"❌ Error conectando con MariaDB: {e}")
        return None
