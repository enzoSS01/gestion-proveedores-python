from mod7_validacion import pedir_opcion_valida, confirmar_si_no
from mod9_comprobantes import comprobante_baja_proveedor
from utilidades import limpiar_pantalla

def eliminar_proveedor(conexion):
    limpiar_pantalla()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, direccion, telefono, email FROM proveedores ORDER BY nombre")
        proveedores = cursor.fetchall()
        if not proveedores:
            print("📭 No hay proveedores registrados.")
            input("Presione Enter para continuar...")
            return

        print("\n📋 Proveedores disponibles:")
        print("-" * 110)
        print(f"{'ID':<4} {'Nombre':<30} {'Teléfono':<18} {'Email':<30} {'Dirección':<35}")
        print("-" * 110)

        for id_, nombre, direccion, telefono, email in proveedores:
            nombre_fmt = (nombre[:27] + '...') if len(nombre) > 30 else nombre
            direccion_fmt = (direccion[:32] + '...') if len(direccion) > 35 else direccion
            telefono_fmt = (telefono[:15] + '...') if telefono and len(telefono) > 18 else (telefono or "")
            email_fmt = (email[:27] + '...') if email and len(email) > 30 else (email or "")
            print(f"{id_:<4} {nombre_fmt:<30} {telefono_fmt:<18} {email_fmt:<30} {direccion_fmt:<35}")

        print("-" * 110)
        print("\n💡 Puede escribir 'CANCELAR' en cualquier momento para volver al menú de proveedores.\n")

        ids_validos = [str(id_) for id_, *_ in proveedores]
        opcion = pedir_opcion_valida("Ingrese el ID del proveedor a eliminar: ", ids_validos)
        if opcion is None or opcion.upper() == "CANCELAR":
            print("↩️ Operación cancelada. Volviendo al menú de proveedores.")
            input("Presione Enter para continuar...")
            return
        id_prov = int(opcion)

        cursor.execute("SELECT nombre, direccion, telefono, email FROM proveedores WHERE id = ?", (id_prov,))
        proveedor = cursor.fetchone()
        if not proveedor:
            print("❌ Proveedor no encontrado.")
            input("Presione Enter para continuar...")
            return

        nombre, direccion, telefono, email = proveedor

        print(f"\n⚠️ Está por eliminar al siguiente proveedor:")
        print(f"🏢 Nombre: {nombre}")
        print(f"📍 Dirección: {direccion}")
        print(f"📞 Teléfono: {telefono}")
        print(f"📧 Email: {email}")
        if not confirmar_si_no("¿Confirma la eliminación?"):
            print("❌ Operación cancelada. Volviendo al menú de proveedores.")
            input("Presione Enter para continuar...")
            return

        cursor.execute("DELETE FROM proveedores WHERE id = ?", (id_prov,))
        conexion.commit()

        comprobante_baja_proveedor(id_prov, nombre, telefono, email, direccion)
        print("\n✅ Proveedor eliminado correctamente.")
        input("\nPresione Enter para volver al menú anterior...")

    except Exception as e:
        print(f"❌ Error al eliminar proveedor: {e}")
        input("Presione Enter para continuar...")