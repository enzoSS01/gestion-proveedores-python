from mod8_ipc import ajustar_precio
from mod7_validacion import confirmar_si_no, pedir_valor_numerico_valido
from decimal import Decimal
from mod9_comprobantes import comprobante_modificacion_ipc
from utilidades import limpiar_pantalla

def actualizar_precios_por_ipc(conexion, variacion_ipc=None):
    limpiar_pantalla()
    try:
        # Si no se pasa variación, pedirla al usuario con validación
        if variacion_ipc is None:
            variacion_ipc = pedir_valor_numerico_valido(
                "Ingrese variación IPC (%): ",
                tipo=Decimal,
                condicion=lambda x: True
            )
            if variacion_ipc is None:
                print("❌ Operación cancelada.")
                input("Presione Enter para continuar...")
                return
        else:
            try:
                variacion_ipc = Decimal(str(variacion_ipc))
            except Exception:
                print("❌ IPC inválido. Debe ser un número decimal.")
                input("Presione Enter para continuar...")
                return

        print(f"\n⚠️ Esta acción actualizará todos los precios registrados con un IPC de {variacion_ipc}%.")
        if not confirmar_si_no("¿Confirma aplicar el IPC a todos los productos?"):
            print("❌ Operación cancelada.")
            input("Presione Enter para continuar...")
            return

        cursor = conexion.cursor()
        cursor.execute("""
            SELECT pr.id, pr.id_producto, p.nombre, pr.precio
            FROM precios pr
            JOIN productos p ON pr.id_producto = p.id
        """)
        precios = cursor.fetchall()

        if not precios:
            print("📭 No hay precios registrados.")
            input("Presione Enter para continuar...")
            return

        lista_de_cambios = []

        for id_precio, id_producto, nombre_producto, precio_actual in precios:
            try:
                precio_decimal = Decimal(str(precio_actual))
                nuevo_precio = ajustar_precio(precio_decimal, variacion_ipc)
                cursor.execute("UPDATE precios SET precio = ? WHERE id = ?", (nuevo_precio, id_precio))
                lista_de_cambios.append((id_producto, nombre_producto, float(precio_decimal), float(nuevo_precio)))
            except Exception as e:
                print(f"❌ Error actualizando producto {id_producto}: {e}")

        conexion.commit()
        comprobante_modificacion_ipc(variacion_ipc, lista_de_cambios)
        print("\n✅ Precios actualizados correctamente.")
        input("\nPresione Enter para volver al menú anterior...")

    except Exception as e:
        print(f"❌ Error al actualizar precios: {e}")
        input("Presione Enter para continuar...")