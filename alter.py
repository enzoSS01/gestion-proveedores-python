import mariadb
from mod1_conectar import conectar
from mod3_lista_proveedores import lista_proveedores

def reset_auto_increment():
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("ALTER TABLE proveedores AUTO_INCREMENT = 1")
        conexion.commit()
        print("🔁 AUTO_INCREMENT reiniciado correctamente.")
    except Exception as e:
        print(f"❌ Error al reiniciar AUTO_INCREMENT: {e}")
    finally:
        conexion.close()
        print("🔒 Conexión cerrada.")

# Ejecutar directamente
if __name__ == "__main__":
    reset_auto_increment()
