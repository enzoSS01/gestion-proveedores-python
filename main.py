#main.py 
from mod0_autenticacion import login
from mod1_conectar import conectar
from mod3_lista_proveedores import lista_proveedores
from mod4_agregar_proveedor import agregar_proveedor
from mod5_actualizar_proveedor import modificar_proveedor
from mod6_eliminar_proveedor import eliminar_proveedor
from mod10_actualizar_precios_ipc import actualizar_precios_por_ipc
from mod11_actualizar_precios_por_proveedor import actualizar_precios_por_proveedor
from mod14_productos import agregar_producto, modificar_producto, eliminar_producto, listar_productos
from mod7_validacion import pedir_opcion_valida, pedir_valor_numerico_valido
from utilidades import limpiar_pantalla

def mostrar_menu_principal():
    limpiar_pantalla()
    print("=== MENÚ PRINCIPAL ===")
    # opciones...

def menu_proveedores(conexion):
    while True:
        limpiar_pantalla()
        print("\n📦 Menú Proveedores")
        print("1. Listar proveedores")
        print("2. Agregar proveedor")
        print("3. Modificar proveedor")
        print("4. Eliminar proveedor")
        print("0. Volver")

        opcion = pedir_opcion_valida("Seleccione una opción: ", ["0", "1", "2", "3", "4"])
        if opcion is None:  # demasiados intentos
            break

        if opcion == "1":
            lista_proveedores(conexion)
        elif opcion == "2":
            agregar_proveedor(conexion)
        elif opcion == "3":
            modificar_proveedor(conexion)
        elif opcion == "4":
            eliminar_proveedor(conexion)
        elif opcion == "0":
            break

def menu_productos(conexion):
    while True:
        limpiar_pantalla()
        print("\n🛒 Menú Productos")
        print("1. Listar productos")
        print("2. Agregar producto")
        print("3. Modificar producto")
        print("4. Eliminar producto")
        print("0. Volver")

        opcion = pedir_opcion_valida("Seleccione una opción: ", ["0", "1", "2", "3", "4"])
        if opcion is None:
            break

        if opcion == "1":
            listar_productos(conexion)
        elif opcion == "2":
            agregar_producto(conexion)
        elif opcion == "3":
            modificar_producto(conexion)
        elif opcion == "4":
            eliminar_producto(conexion)
        elif opcion == "0":
            break

def menu_precios(conexion):
    while True:
        limpiar_pantalla()
        print("\n💰 Menú Precios")
        print("1. Ajustar precios por IPC (global)")
        print("2. Ajustar precios por proveedor")
        print("0. Volver")

        opcion = pedir_opcion_valida("Seleccione una opción: ", ["0", "1", "2"])
        if opcion is None:
            break

        if opcion == "1":
            ipc_float = pedir_valor_numerico_valido("Ingrese variación IPC (%): ", float, lambda x: True)
            if ipc_float is not None:
                actualizar_precios_por_ipc(conexion, ipc_float)
        elif opcion == "2":
            actualizar_precios_por_proveedor(conexion)
        elif opcion == "0":
            break

def menu_principal_admin(conexion):
    while True:
        limpiar_pantalla()
        print("\n🧭 Menú Principal")
        print("1. Proveedores")
        print("2. Productos")
        print("3. Actualizar Precios")
        print("0. Salir")

        opcion = pedir_opcion_valida("Seleccione una opción: ", ["0", "1", "2", "3"])
        if opcion is None:
            break

        if opcion == "1":
            menu_proveedores(conexion)
        elif opcion == "2":
            menu_productos(conexion)
        elif opcion == "3":
            menu_precios(conexion)
        elif opcion == "0":
            print("👋 Cerrando sesión...")
            break

def menu_principal_consulta(conexion):
    while True:
        limpiar_pantalla()
        print("\n📋 Menú Consulta")
        print("1. Listar proveedores")
        print("2. Agregar proveedor")
        print("3. Listar productos")
        print("4. Agregar producto")
        print("0. Salir")

        opcion = pedir_opcion_valida("Seleccione una opción: ", ["0", "1", "2", "3", "4"])
        if opcion is None:
            break

        if opcion == "1":
            lista_proveedores(conexion)
        elif opcion == "2":
            agregar_proveedor(conexion)
        elif opcion == "3":
            listar_productos(conexion)
        elif opcion == "4":
            agregar_producto(conexion)
        elif opcion == "0":
            print("👋 Cerrando sesión...")
            break

def main():
    sesion = login()
    if not sesion:
        return

    conexion = conectar()
    if not conexion:
        return

    if sesion["rol"] == "admin":
        menu_principal_admin(conexion)
    else:
        menu_principal_consulta(conexion)

    conexion.close()

if __name__ == "__main__":
    main()
