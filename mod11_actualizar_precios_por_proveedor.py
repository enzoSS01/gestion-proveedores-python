from decimal import Decimal
from mod7_validacion import pedir_opcion_valida, confirmar_si_no, pedir_valor_numerico_valido
from mod9_comprobantes import comprobante_modificacion_por_proveedor
from utilidades import limpiar_pantalla

def actualizar_precios_por_proveedor(conexion):
    limpiar_pantalla()
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre FROM proveedores ORDER BY nombre")
        proveedores = cursor.fetchall()

        if not proveedores:
            print("📭 No hay proveedores registrados.")
            input("Presione Enter para continuar...")
            return

        print("\n📋 Proveedores disponibles:")
        print("-" * 35)
        print(f"{'ID':<5} {'Nombre':<30}")
        print("-" * 35)
        for id_, nombre in proveedores:
            print(f"{id_:<5} {nombre:<30}")
        print("-" * 35)

        ids_validos = [str(id_) for id_, _ in proveedores]
        opcion = pedir_opcion_valida("Ingrese el ID del proveedor a ajustar: ", ids_validos)
        if opcion is None:
            print("↩️ Operación cancelada. Volviendo al menú de precios.")
            input("Presione Enter para continuar...")
            return
        id_proveedor = int(opcion)

        cursor.execute("SELECT nombre FROM proveedores WHERE id = ?", (id_proveedor,))
        prov = cursor.fetchone()
        if not prov:
            print("❌ Proveedor no encontrado.")
            input("Presione Enter para continuar...")
            return
        nombre_proveedor = prov[0]

        cursor.execute("""
            SELECT pr.id, pr.id_producto, pr.precio, p.nombre
            FROM precios pr
            JOIN productos p ON pr.id_producto = p.id
            WHERE pr.id_proveedor = ?
        """, (id_proveedor,))
        precios = cursor.fetchall()

        if not precios:
            print("📭 Este proveedor no tiene precios registrados.")
            input("Presione Enter para continuar...")
            return

        porcentaje = pedir_valor_numerico_valido(
            "Ingrese porcentaje de ajuste (ej: 10 para +10%, -5 para -5%): ",
            tipo=Decimal,
            condicion=lambda x: True
        )
        if porcentaje is None:
            print("❌ Operación cancelada.")
            input("Presione Enter para continuar...")
            return
        ajuste = porcentaje / Decimal(100)

        print(f"\n⚠️ Esta acción actualizará todos los precios del proveedor '{nombre_proveedor}' con un ajuste de {porcentaje}%.")
        if not confirmar_si_no("¿Confirma aplicar el ajuste?"):
            print("❌ Operación cancelada.")
            input("Presione Enter para continuar...")
            return

        lista_de_cambios = []

        for id_precio, id_producto, precio_actual, nombre_producto in precios:
            try:
                nuevo_precio = round(precio_actual * (1 + ajuste), 2)
                cursor.execute("UPDATE precios SET precio = ? WHERE id = ?", (nuevo_precio, id_precio))
                lista_de_cambios.append((id_producto, nombre_producto, float(precio_actual), float(nuevo_precio)))
            except Exception as e:
                print(f"❌ Error actualizando producto {id_producto}: {e}")

        conexion.commit()
        comprobante_modificacion_por_proveedor(id_proveedor, nombre_proveedor, str(porcentaje), lista_de_cambios)
        print("\n✅ Precios actualizados correctamente.")
        input("\nPresione Enter para volver al menú anterior...")

    except Exception as e:
        print(f"❌ Error al actualizar precios: {e}")
        input("Presione Enter para continuar...")