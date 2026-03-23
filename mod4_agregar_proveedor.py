from mod7_validacion import (
    validar_nombre, validar_telefono, validar_email,
    validar_direccion, confirmar_si_no, pedir_texto_no_vacio
)
from mod9_comprobantes import comprobante_alta_proveedor
from utilidades import limpiar_pantalla

def agregar_proveedor(conexion):
    limpiar_pantalla()
    try:
        cursor = conexion.cursor()
        print("\n=== 🧾 ALTA DE PROVEEDOR ===")
        print("💡 Puede escribir 'CANCELAR' en cualquier momento para volver al menú de proveedores.\n")

        nombre = pedir_texto_no_vacio(
            "🏢 Nombre del proveedor: ",
            condicion=lambda x: validar_nombre(x) and len(x) >= 3,
            mensaje_error="❌ Nombre inválido. Debe tener al menos 3 caracteres y solo letras/espacios."
        )
        if nombre in (None, "CANCELAR"):
            print("↩️ Operación cancelada. Volviendo al menú de proveedores.")
            input("Presione Enter para continuar...")
            return

        cursor.execute("SELECT id FROM proveedores WHERE nombre = ?", (nombre,))
        if cursor.fetchone():
            print("⚠️ Ya existe un proveedor con ese nombre.")
            if not confirmar_si_no("¿Desea intentar con otro nombre?"):
                print("↩️ Volviendo al menú de proveedores.")
                input("Presione Enter para continuar...")
                return
            return agregar_proveedor(conexion)

        direccion = pedir_texto_no_vacio(
            "📍 Dirección: ",
            condicion=validar_direccion,
            mensaje_error="❌ Dirección inválida. Debe tener al menos 5 caracteres."
        )
        if direccion in (None, "CANCELAR"):
            print("↩️ Operación cancelada. Volviendo al menú de proveedores.")
            input("Presione Enter para continuar...")
            return

        telefono = pedir_texto_no_vacio(
            "📞 Teléfono: ",
            condicion=validar_telefono,
            mensaje_error="❌ Teléfono inválido. Debe tener entre 6 y 15 dígitos."
        )
        if telefono in (None, "CANCELAR"):
            print("↩️ Operación cancelada. Volviendo al menú de proveedores.")
            input("Presione Enter para continuar...")
            return

        email = pedir_texto_no_vacio(
            "📧 Email: ",
            condicion=validar_email,
            mensaje_error="❌ Email inválido. Intente nuevamente."
        )
        if email in (None, "CANCELAR"):
            print("↩️ Operación cancelada. Volviendo al menú de proveedores.")
            input("Presione Enter para continuar...")
            return

        print("\n📋 Resumen del proveedor a registrar:")
        print(f"🏢 Nombre: {nombre}")
        print(f"📍 Dirección: {direccion}")
        print(f"📞 Teléfono: {telefono}")
        print(f"📧 Email: {email}")

        if not confirmar_si_no("¿Desea confirmar el alta del proveedor?"):
            print("❌ Operación cancelada. Volviendo al menú de proveedores.")
            input("Presione Enter para continuar...")
            return

        cursor.execute("""
            INSERT INTO proveedores (nombre, direccion, telefono, email)
            VALUES (?, ?, ?, ?)
        """, (nombre, direccion, telefono, email))
        conexion.commit()

        id_prov = cursor.lastrowid
        comprobante_alta_proveedor(id_prov, nombre, telefono, email, direccion)

        print("\n✅ Proveedor agregado correctamente.")
        input("\nPresione Enter para volver al menú anterior...")

    except Exception as e:
        print(f"❌ Error al agregar proveedor: {e}")
        input("Presione Enter para continuar...")