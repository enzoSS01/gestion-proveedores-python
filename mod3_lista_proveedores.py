from utilidades import limpiar_pantalla
def lista_proveedores(conexion):
    limpiar_pantalla()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, nombre, direccion, telefono, email
            FROM proveedores
            ORDER BY nombre
        """)
        proveedores = cursor.fetchall()

        if not proveedores:
            print("📭 No hay proveedores registrados.")
            return

        print("\n📋 Lista de proveedores:")
        print("-" * 110)
        print(f"{'ID':<4} {'Nombre':<30} {'Teléfono':<18} {'Email':<30} {'Dirección':<35}")
        print("-" * 110)
        for id_, nombre, direccion, telefono, email in proveedores:
            nombre_fmt = (nombre[:27] + '...') if len(nombre) > 30 else nombre
            direccion_fmt = (direccion[:32] + '...') if len(direccion) > 35 else direccion
            telefono_fmt = telefono or ""
            email_fmt = email or ""
            print(f"{id_:<4} {nombre_fmt:<30} {telefono_fmt:<18} {email_fmt:<30} {direccion_fmt:<35}")

        print("-" * 110)
        print(f"🔢 Total de proveedores: {len(proveedores)}")
        input("\nPresione ENTER para volver al menú anterior...")


    except Exception as e:
        print(f"❌ Error al listar proveedores: {e}")