#mod1_conectar.py
import mariadb

def conectar():
    try:
        conexion = mariadb.connect(
            user="root",
            password="123456",
            host="localhost",
            port=3306,
            database="control_proveedores"
        )
        return conexion
    except mariadb.Error as e:
        print(f"❌ Error conectando con MariaDB: {e}")
        return None