# mod14_productos.py
from decimal import Decimal, InvalidOperation
from mod7_validacion import (
    confirmar_si_no, validar_nombre, pedir_texto_no_vacio
)
from mod9_comprobantes import comprobante_alta_producto, comprobante_baja_producto, comprobante_modificacion_producto
from utilidades import limpiar_pantalla

def agregar_producto(conexion):
    limpiar_pantalla()
    try:
        cursor = conexion.cursor()
        print("\n💡 Puede escribir 'CANCELAR' en cualquier momento para volver al menú de productos.\n")

        nombre = pedir_texto_no_vacio(
            "📦 Nombre del producto: ",
            condicion=lambda x: validar_nombre(x) and len(x) >= 3,
            mensaje_error="❌ Nombre inválido. Debe tener al menos 3 caracteres y solo letras/espacios."
        )
        if nombre in (None, "CANCELAR"):
            print("↩️ Operación cancelada.")
            input("Presione Enter para continuar...")
            return

        descripcion = pedir_texto_no_vacio(
            "📝 Descripción: ",
            condicion=lambda x: len(x) >= 3,
            mensaje_error="❌ Descripción demasiado corta. Debe tener al menos 3 caracteres."
        )
        if descripcion in (None, "CANCELAR"):
            print("↩️ Operación cancelada.")
            input("Presione Enter para continuar...")
            return

        categoria = pedir_texto_no_vacio(
            "📂 Categoría: ",
            condicion=lambda x: len(x) >= 3,
            mensaje_error="❌ Categoría inválida. Debe tener al menos 3 caracteres."
        )
        if categoria in (None, "CANCELAR"):
            print("↩️ Operación cancelada.")
            input("Presione Enter para continuar...")
            return

        cursor.execute("SELECT id, nombre FROM proveedores ORDER BY nombre")
        proveedores = cursor.fetchall()
        if not proveedores:
            print("📭 No hay proveedores registrados.")
            input("Presione Enter para continuar...")
            return

        print("\n📋 Proveedores disponibles:")
        for id_, nombre_prov in proveedores:
            print(f"{id_}. {nombre_prov}")
        ids_validos = [str(id_) for id_, _ in proveedores]

        from mod7_validacion import pedir_opcion_valida
        opcion = pedir_opcion_valida("Ingrese el ID del proveedor: ", ids_validos)
        if opcion in (None, "CANCELAR"):
            print("↩️ Operación cancelada.")
            input("Presione Enter para continuar...")
            return
        id_proveedor = int(opcion)

        cursor.execute("SELECT nombre FROM proveedores WHERE id = ?", (id_proveedor,))
        proveedor = cursor.fetchone()
        if not proveedor:
            print("❌ Proveedor no encontrado.")
            input("Presione Enter para continuar...")
            return
        proveedor_nombre = proveedor[0]

        from mod7_validacion import pedir_valor_numerico_valido
        precio = pedir_valor_numerico_valido(
            "💲 Precio: ",
            tipo=Decimal,
            condicion=lambda x: x > 0
        )
        if precio is None:
            print("↩️ Operación cancelada.")
            input("Presione Enter para continuar...")
            return
        precio = precio.quantize(Decimal("0.01"))

        from mod7_validacion import pedir_entero_positivo
        stock = pedir_entero_positivo("📦 Stock inicial: ")
        if stock is None:
            print("↩️ Operación cancelada.")
            input("Presione Enter para continuar...")
            return

        if not confirmar_si_no("¿Confirma el alta del producto?"):
            print("❌ Operación cancelada.")
            input("Presione Enter para continuar...")
            return

        cursor.execute("""
            INSERT INTO productos (nombre, descripcion, categoria, proveedor_id, stock)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, descripcion, categoria, id_proveedor, stock))
        conexion.commit()

        id_producto = cursor.lastrowid
        cursor.execute("""
            INSERT INTO precios (id_producto, id_proveedor, precio)
            VALUES (?, ?, ?)
        """, (id_producto, id_proveedor, float(precio)))
        conexion.commit()

        comprobante_alta_producto(id_producto, nombre, categoria, stock, float(precio), proveedor_nombre)
        print("\n✅ Producto agregado correctamente.")
        input("\nPresione Enter para volver al menú anterior...")

    except Exception as e:
        print(f"❌ Error al agregar producto: {e}")
        input("Presione Enter para continuar...")


from decimal import Decimal
from mod7_validacion import (
    validar_nombre, confirmar_si_no,
    pedir_opcion_valida, pedir_texto_opcional,
    pedir_entero_opcional, pedir_valor_numerico_valido
)
from mod9_comprobantes import comprobante_modificacion_producto
from utilidades import limpiar_pantalla

def modificar_producto(conexion):
    limpiar_pantalla()
    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT p.id, p.nombre, p.categoria, p.stock,
                   r.precio, pr.nombre
            FROM productos p
            JOIN proveedores pr ON p.proveedor_id = pr.id
            LEFT JOIN precios r ON r.id_producto = p.id AND r.id_proveedor = pr.id
            ORDER BY p.id
        """)
        productos = cursor.fetchall()
        if not productos:
            print("📭 No hay productos registrados.")
            input("Presione Enter para continuar...")
            return

        print("\n📦 Lista de productos:")
        print("-" * 86)
        print(f"{'ID':<4} {'Nombre':<30} {'Categoría':<15} {'Stock':>7} {'Precio':>10}   {'Proveedor':<20}")
        print("-" * 86)
        for id_, nombre, categoria, stock, precio, proveedor in productos:
            nombre_fmt = (nombre[:27] + '...') if len(nombre) > 30 else nombre
            precio_fmt = f"${precio:.2f}" if precio is not None else "Sin precio"
            print(f"{id_:<4} {nombre_fmt:<30} {categoria:<15} {stock:>7} {precio_fmt:>10}   {proveedor:<20}")
        print("-" * 86)

        print("\n💡 Puede escribir 'CANCELAR' en cualquier momento para volver al menú de productos.\n")

        ids_validos = [str(id_) for id_, *_ in productos]
        opcion = pedir_opcion_valida("Ingrese el ID del producto a modificar: ", ids_validos)
        if opcion is None or opcion.upper() == "CANCELAR":
            print("↩️ Operación cancelada.")
            input("Presione Enter para continuar...")
            return
        id_producto = int(opcion)

        cursor.execute("""
            SELECT p.nombre, p.descripcion, p.categoria, p.stock,
                   pr.id AS proveedor_id, pr.nombre AS proveedor_nombre,
                   r.precio
            FROM productos p
            JOIN proveedores pr ON p.proveedor_id = pr.id
            LEFT JOIN precios r ON r.id_producto = p.id AND r.id_proveedor = pr.id
            WHERE p.id = ?
        """, (id_producto,))
        producto = cursor.fetchone()
        if not producto:
            print("❌ Producto no encontrado.")
            input("Presione Enter para continuar...")
            return

        nombre_ant, desc_ant, cat_ant, stock_ant, proveedor_id, proveedor_nombre, precio_ant = producto
        cambios = []

        print("\n✏️ Ingrese los nuevos valores (dejar vacío para mantener):")

        nombre_nuevo = pedir_texto_opcional(
            "📦 Nombre ",
            nombre_ant,
            condicion=lambda x: validar_nombre(x) and len(x) >= 3,
            max_intentos=3
        )
        if nombre_nuevo == "CANCELAR":
            print("↩️ Operación cancelada.")
            input("Presione Enter para continuar...")
            return

        descripcion = pedir_texto_opcional(
            "📝 Descripción ",
            desc_ant,
            condicion=lambda x: len(x) >= 3,
            max_intentos=3
        )
        if descripcion == "CANCELAR":
            print("↩️ Operación cancelada.")
            input("Presione Enter para continuar...")
            return

        categoria = pedir_texto_opcional(
            "📂 Categoría ",
            cat_ant,
            condicion=lambda x: len(x) >= 3,
            max_intentos=3
        )
        if categoria == "CANCELAR":
            print("↩️ Operación cancelada.")
            input("Presione Enter para continuar...")
            return

        stock_nuevo = pedir_entero_opcional("📦 Stock ", stock_ant)
        if stock_nuevo == "CANCELAR":
            print("↩️ Operación cancelada.")
            input("Presione Enter para continuar...")
            return

        precio_input = input(f"💲 Precio [{precio_ant if precio_ant else 'Sin precio'}]: ").strip()
        if precio_input.upper() == "CANCELAR":
            print("↩️ Operación cancelada.")
            input("Presione Enter para continuar...")
            return
        if precio_input == "":
            precio_nuevo = precio_ant
        else:
            precio_nuevo = pedir_valor_numerico_valido("💲 Precio: ", Decimal, lambda x: x > 0)
            if precio_nuevo is None:
                print("❌ Operación cancelada.")
                input("Presione Enter para continuar...")
                return
            precio_nuevo = precio_nuevo.quantize(Decimal("0.01"))

        if nombre_nuevo != nombre_ant:
            cambios.append(("Nombre", nombre_ant, nombre_nuevo))
        if descripcion != desc_ant:
            cambios.append(("Descripción", desc_ant, descripcion))
        if categoria != cat_ant:
            cambios.append(("Categoría", cat_ant, categoria))
        if stock_nuevo != stock_ant:
            cambios.append(("Stock", stock_ant, stock_nuevo))
        if precio_nuevo != precio_ant:
            cambios.append(("Precio", precio_ant if precio_ant is not None else "Sin precio",
                            float(precio_nuevo) if precio_nuevo is not None else "Sin precio"))

        if not cambios:
            print("ℹ️ No se realizaron cambios.")
            input("\nPresione Enter para volver al menú anterior...")
            return

        print("\n📋 Resumen de cambios:")
        for campo, antes, despues in cambios:
            print(f"🔄 {campo}: '{antes}' → '{despues}'")
        if not confirmar_si_no("¿Confirma la modificación?"):
            print("❌ Operación cancelada.")
            input("Presione Enter para continuar...")
            return

        cursor.execute("""
            UPDATE productos
            SET nombre = ?, descripcion = ?, categoria = ?, stock = ?
            WHERE id = ?
        """, (nombre_nuevo, descripcion, categoria, stock_nuevo, id_producto))
        conexion.commit()

        cursor.execute("""
            UPDATE precios
            SET precio = ?
            WHERE id_producto = ? AND id_proveedor = ?
        """, (float(precio_nuevo) if precio_nuevo is not None else None, id_producto, proveedor_id))
        conexion.commit()

        limpiar_pantalla()
        print("✅ Modificación realizada correctamente.")
        comprobante_modificacion_producto(id_producto, cambios)
        input("\nPresione Enter para volver al menú anterior...")

    except Exception as e:
        print(f"❌ Error al modificar producto: {e}")
        input("Presione Enter para continuar...")

def eliminar_producto(conexion):
    limpiar_pantalla()
    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT p.id, p.nombre, p.categoria, p.stock,
                   r.precio, pr.nombre
            FROM productos p
            JOIN proveedores pr ON p.proveedor_id = pr.id
            LEFT JOIN precios r ON r.id_producto = p.id AND r.id_proveedor = pr.id
            ORDER BY p.id
        """)
        productos = cursor.fetchall()
        if not productos:
            print("📭 No hay productos registrados.")
            input("Presione Enter para continuar...")
            return

        print("\n📦 Lista de productos:")
        print("-" * 86)
        print(f"{'ID':<4} {'Nombre':<30} {'Categoría':<15} {'Stock':>7} {'Precio':>10}   {'Proveedor':<20}")
        print("-" * 86)
        for id_, nombre, categoria, stock, precio, proveedor in productos:
            nombre_fmt = (nombre[:27] + '...') if len(nombre) > 30 else nombre
            precio_fmt = f"${precio:.2f}" if precio is not None else "Sin precio"
            print(f"{id_:<4} {nombre_fmt:<30} {categoria:<15} {stock:>7} {precio_fmt:>10}   {proveedor:<20}")
        print("-" * 86)

        print("\n💡 Puede escribir 'CANCELAR' en cualquier momento para volver al menú de productos.\n")

        ids_validos = [str(id_) for id_, *_ in productos]
        opcion = pedir_opcion_valida("Ingrese el ID del producto a eliminar: ", ids_validos)
        if opcion is None or opcion.upper() == "CANCELAR":
            print("↩️ Operación cancelada. Volviendo al menú de productos.")
            input("Presione Enter para continuar...")
            return
        id_producto = int(opcion)

        cursor.execute("""
            SELECT p.nombre, p.categoria, p.stock,
                   r.precio, pr.nombre
            FROM productos p
            JOIN proveedores pr ON p.proveedor_id = pr.id
            LEFT JOIN precios r ON r.id_producto = p.id AND r.id_proveedor = pr.id
            WHERE p.id = ?
        """, (id_producto,))
        producto = cursor.fetchone()
        if not producto:
            print("❌ Producto no encontrado.")
            input("Presione Enter para continuar...")
            return

        nombre, categoria, stock, precio, proveedor = producto
        precio_str = f"${precio:.2f}" if precio is not None else "Sin precio"

        print(f"\n⚠️ Está por eliminar el producto: {nombre} ({proveedor})")
        print(f"📂 Categoría: {categoria} | 💲 Precio: {precio_str} | 📦 Stock: {stock}")
        if not confirmar_si_no("¿Confirma la eliminación?"):
            print("❌ Operación cancelada. Volviendo al menú de productos.")
            input("Presione Enter para continuar...")
            return

        cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
        cursor.execute("DELETE FROM precios WHERE id_producto = ?", (id_producto,))
        conexion.commit()

        comprobante_baja_producto(id_producto, nombre, categoria, stock, precio, proveedor)
        print("\n✅ Producto eliminado correctamente.")
        input("\nPresione Enter para volver al menú anterior...")

    except Exception as e:
        print(f"❌ Error al eliminar producto: {e}")
        input("Presione Enter para continuar...")

def listar_productos(conexion):
    limpiar_pantalla()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT p.id, p.nombre, p.categoria, p.stock,
                   r.precio, pr.nombre
            FROM productos p
            JOIN proveedores pr ON p.proveedor_id = pr.id
            LEFT JOIN precios r ON r.id_producto = p.id AND r.id_proveedor = pr.id
            ORDER BY p.id
        """)
        productos = cursor.fetchall()
        if not productos:
            print("📭 No hay productos registrados.")
            input("Presione ENTER para volver al menú anterior....")
            return

        print("\n📦 Lista de productos:")
        print("-" * 86)
        print(f"{'ID':<4} {'Nombre':<30} {'Categoría':<15} {'Stock':>7} {'Precio':>10}   {'Proveedor':<20}")
        print("-" * 86)

        for id_, nombre, categoria, stock, precio, proveedor in productos:
            nombre_fmt = (nombre[:27] + '...') if len(nombre) > 30 else nombre
            precio_fmt = f"${precio:.2f}" if precio is not None else "Sin precio"
            print(f"{id_:<4} {nombre_fmt:<30} {categoria:<15} {stock:>7} {precio_fmt:>10}   {proveedor:<20}")

        print("-" * 86)
        input("\nPresione ENTER para volver al menú anterior...")

    except Exception as e:
        print(f"❌ Error al listar productos: {e}")
