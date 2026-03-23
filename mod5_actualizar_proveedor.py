from mod7_validacion import (
    validar_nombre, validar_telefono, validar_email,
    validar_direccion, confirmar_si_no, pedir_opcion_valida, pedir_texto_opcional
)
from mod9_comprobantes import comprobante_modificacion_proveedor
from utilidades import limpiar_pantalla

def modificar_proveedor(conexion):
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
            print(f"{id_:<4} {nombre:<30} {telefono:<18} {email:<30} {direccion:<35}")
        print("-" * 110)

        opcion = pedir_opcion_valida("Ingrese el ID del proveedor a modificar: ", [str(id_) for id_, *_ in proveedores])
        if opcion in (None, "CANCELAR"):
            print("↩️ Operación cancelada.")
            input("Presione Enter para continuar...")
            return
        id_prov = int(opcion)

        cursor.execute("SELECT nombre, direccion, telefono, email FROM proveedores WHERE id = ?", (id_prov,))
        proveedor = cursor.fetchone()
        if not proveedor:
            print("❌ Proveedor no encontrado.")
            input("Presione Enter para continuar...")
            return

        nombre_actual, direccion_actual, telefono_actual, email_actual = proveedor

        nombre = pedir_texto_opcional(
            "🏢 Nombre ",
            nombre_actual,
            condicion=lambda x: validar_nombre(x) and len(x) >= 3,
            max_intentos=3
        )
        if nombre == "CANCELAR":
            print("↩️ Operación cancelada.")
            input("Presione Enter para continuar...")
            return

        direccion = pedir_texto_opcional(
            "📍 Dirección ",
            direccion_actual,
            condicion=validar_direccion,
            max_intentos=3
        )
        if direccion == "CANCELAR":
            print("↩️ Operación cancelada.")
            input("Presione Enter para continuar...")
            return

        telefono = pedir_texto_opcional(
            "📞 Teléfono ",
            telefono_actual,
            condicion=validar_telefono,
            max_intentos=3
        )
        if telefono == "CANCELAR":
            print("↩️ Operación cancelada.")
            input("Presione Enter para continuar...")
            return

        email = pedir_texto_opcional(
            "📧 Email ",
            email_actual,
            condicion=validar_email,
            max_intentos=3
        )
        if email == "CANCELAR":
            print("↩️ Operación cancelada.")
            input("Presione Enter para continuar...")
            return

        cambios = []
        if nombre != nombre_actual:
            cambios.append(("Nombre", nombre_actual, nombre))
        if direccion != direccion_actual:
            cambios.append(("Dirección", direccion_actual, direccion))
        if telefono != telefono_actual:
            cambios.append(("Teléfono", telefono_actual, telefono))
        if email != email_actual:
            cambios.append(("Email", email_actual, email))

        if not cambios:
            print("ℹ️ No se realizaron modificaciones.")
            input("Presione Enter para continuar...")
            return

        print("\n📋 Resumen de cambios:")
        for campo, antes, despues in cambios:
            print(f"🔄 {campo}: '{antes}' → '{despues}'")
        if not confirmar_si_no("¿Confirma la modificación?"):
            print("❌ Operación cancelada.")
            input("Presione Enter para continuar...")
            return

        cursor.execute("""
            UPDATE proveedores
            SET nombre = ?, direccion = ?, telefono = ?, email = ?
            WHERE id = ?
        """, (nombre, direccion, telefono, email, id_prov))
        conexion.commit()

        comprobante_modificacion_proveedor(id_prov, cambios)
        print("\n✅ Modificación realizada correctamente.")
        input("Presione Enter para volver al menú anterior...")

    except Exception as e:
        print(f"❌ Error al modificar proveedor: {e}")
        input("Presione Enter para continuar...")