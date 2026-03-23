from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import datetime

def guardar_comprobante_pdf(
    texto,
    nombre_archivo="comprobante.pdf",
    alineado=False,
    margen_izq=50,
    margen_sup=50,
    interlineado=20
):
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c = canvas.Canvas(nombre_archivo, pagesize=A4)
    width, height = A4

    c.setFont("Courier", 10)
    y = height - margen_sup
    c.drawString(margen_izq, y, f"Comprobante generado el {fecha}")
    y -= interlineado * 2

    for linea in texto.split('\n'):
        if alineado:
            c.drawRightString(width - margen_izq, y, linea)
        else:
            c.drawString(margen_izq, y, linea)
        y -= interlineado
        if y < margen_sup:
            c.showPage()
            c.setFont("Courier", 10)
            y = height - margen_sup

    c.save()
    print(f"\n✅ Comprobante guardado como '{nombre_archivo}'")

def comprobante_alta_producto(id_producto, nombre, categoria, stock, precio, proveedor):
    nombre_fmt = (nombre[:27] + '...') if len(nombre) > 30 else nombre
    proveedor_fmt = (proveedor[:17] + '...') if len(proveedor) > 20 else proveedor
    precio_fmt = f"${precio:.2f}" if precio is not None else "Sin precio"

    texto = "\n🧾 Comprobante de alta de producto\n"
    texto += "-" * 86 + "\n"
    texto += f"{'ID':<4} {'Nombre':<30} {'Categoría':<15} {'Stock':>7} {'Precio':>10}   {'Proveedor':<20}\n"
    texto += "-" * 86 + "\n"
    texto += f"{id_producto:<4} {nombre_fmt:<30} {categoria:<15} {stock:>7} {precio_fmt:>10}   {proveedor_fmt:<20}\n"

    print(texto)
    if input("¿Guardar como PDF? (s/n): ").lower() == 's':
        nombre = input("Nombre de archivo (sin extensión): ")
        guardar_comprobante_pdf(texto, f"{nombre}.pdf", margen_izq=40, margen_sup=60, interlineado=18)


def comprobante_baja_producto(id_producto, nombre, categoria, stock, precio, proveedor):
    nombre_fmt = (nombre[:27] + '...') if len(nombre) > 30 else nombre
    proveedor_fmt = (proveedor[:17] + '...') if len(proveedor) > 20 else proveedor
    precio_fmt = f"${precio:.2f}" if precio is not None else "Sin precio"

    texto = "\n🧾 Comprobante de baja de producto\n"
    texto += "-" * 86 + "\n"
    texto += f"{'ID':<4} {'Nombre':<30} {'Categoría':<15} {'Stock':>7} {'Precio':>10}   {'Proveedor':<20}\n"
    texto += "-" * 86 + "\n"
    texto += f"{id_producto:<4} {nombre_fmt:<30} {categoria:<15} {stock:>7} {precio_fmt:>10}   {proveedor_fmt:<20}\n"

    print(texto)
    if input("¿Guardar como PDF? (s/n): ").lower() == 's':
        nombre = input("Nombre de archivo (sin extensión): ")
        guardar_comprobante_pdf(texto, f"{nombre}.pdf", margen_izq=40, margen_sup=60, interlineado=18)


def comprobante_alta_proveedor(id_prov, nombre, telefono, email, direccion):
    nombre_fmt = (nombre[:27] + '...') if len(nombre) > 30 else nombre
    direccion_fmt = (direccion[:27] + '...') if len(direccion) > 30 else direccion
    telefono_fmt = (telefono[:17] + '...') if len(telefono) > 20 else telefono
    email_fmt = (email[:27] + '...') if len(email) > 30 else email

    texto = "\n🧾 Comprobante de alta de proveedor\n"
    texto += "-" * 110 + "\n"
    texto += f"{'ID':<4} {'Nombre':<30} {'Teléfono':<20} {'Email':<30} {'Dirección':<30}\n"
    texto += "-" * 110 + "\n"
    texto += f"{id_prov:<4} {nombre_fmt:<30} {telefono_fmt:<20} {email_fmt:<30} {direccion_fmt:<30}\n"

    print(texto)
    if input("¿Guardar como PDF? (s/n): ").lower() == 's':
        nombre = input("Nombre de archivo (sin extensión): ")
        guardar_comprobante_pdf(texto, f"{nombre}.pdf", margen_izq=30, margen_sup=60, interlineado=18)


def comprobante_baja_proveedor(id_prov, nombre, telefono, email, direccion):
    nombre_fmt = (nombre[:27] + '...') if len(nombre) > 30 else nombre
    direccion_fmt = (direccion[:27] + '...') if len(direccion) > 30 else direccion
    telefono_fmt = (telefono[:17] + '...') if len(telefono) > 20 else telefono
    email_fmt = (email[:27] + '...') if len(email) > 30 else email

    texto = "\n🧾 Comprobante de baja de proveedor\n"
    texto += "-" * 110 + "\n"
    texto += f"{'ID':<4} {'Nombre':<30} {'Teléfono':<20} {'Email':<30} {'Dirección':<30}\n"
    texto += "-" * 110 + "\n"
    texto += f"{id_prov:<4} {nombre_fmt:<30} {telefono_fmt:<20} {email_fmt:<30} {direccion_fmt:<30}\n"

    print(texto)
    if input("¿Guardar como PDF? (s/n): ").lower() == 's':
        nombre = input("Nombre de archivo (sin extensión): ")
        guardar_comprobante_pdf(texto, f"{nombre}.pdf", margen_izq=30, margen_sup=60, interlineado=18)

def comprobante_modificacion_proveedor(id_proveedor, cambios):
    texto = f"\n🧾 Comprobante de modificación: Proveedor\n"
    texto += f"Se han realizado los siguientes cambios al proveedor ID {id_proveedor}:\n\n"
    texto += "-" * 78 + "\n"
    texto += f"{'Dato modificado':<18} {'Antes':<30} {'Después':<30}\n"
    texto += "-" * 78 + "\n"
    for etiqueta, antes, despues in cambios:
        texto += f"{etiqueta:<18} {str(antes):<30} {str(despues):<30}\n"
    texto += "-" * 78 + "\n"

    print(texto)
    if input("¿Guardar como PDF? (s/n): ").lower() == 's':
        nombre = input("Nombre de archivo (sin extensión): ")
        guardar_comprobante_pdf(texto, f"{nombre}.pdf", margen_izq=35, margen_sup=60, interlineado=18)

def comprobante_modificacion_producto(id_producto, cambios):
    texto = f"\n🧾 Comprobante de modificación: Producto\n"
    texto += f"Se han realizado los siguientes cambios al producto ID {id_producto}:\n\n"
    texto += "-" * 78 + "\n"
    texto += f"{'Dato modificado':<18} {'Antes':<30} {'Después':<30}\n"
    texto += "-" * 78 + "\n"
    for etiqueta, antes, despues in cambios:
        texto += f"{etiqueta:<18} {str(antes):<30} {str(despues):<30}\n"
    texto += "-" * 78 + "\n"

    print(texto)
    if input("¿Guardar como PDF? (s/n): ").lower() == 's':
        nombre = input("Nombre de archivo (sin extensión): ")
        guardar_comprobante_pdf(texto, f"{nombre}.pdf", margen_izq=35, margen_sup=60, interlineado=18)


def comprobante_modificacion_por_proveedor(id_prov, nombre_prov, porcentaje, cambios):
    texto = f"\n🧾 Comprobante de modificación de precios por proveedor\n"
    texto += f"Proveedor: {id_prov} - {nombre_prov}\n"
    texto += f"Ajuste aplicado: {porcentaje}%\n\n"
    texto += "-" * 73 + "\n"
    texto += f"{'ID':<4} {'Producto':<35} {'Precio anterior':>15} {'Precio nuevo':>15}\n"
    texto += "-" * 73 + "\n"
    cambios_ordenados = sorted(cambios, key=lambda x: x[0])
    for id_prod, nombre, antes, despues in cambios_ordenados:
        nombre_fmt = (nombre[:32] + '...') if len(nombre) > 35 else nombre
        texto += f"{id_prod:<4} {nombre_fmt:<35} {f'${antes:.2f}':>15} {f'${despues:.2f}':>15}\n"
    texto += "-" * 73 + "\n"

    print(texto)
    if input("¿Guardar como PDF? (s/n): ").lower() == 's':
        nombre = input("Nombre de archivo (sin extensión): ")
        guardar_comprobante_pdf(texto, f"{nombre}.pdf", margen_izq=30, margen_sup=60, interlineado=18)


def comprobante_modificacion_ipc(porcentaje, cambios):
    texto = f"\n🧾 Comprobante de modificación de precios por IPC ({porcentaje}%):\n"
    texto += "-" * 73 + "\n"
    texto += f"{'ID':<4} {'Producto':<35} {'Precio anterior':>15} {'Precio nuevo':>15}\n"
    texto += "-" * 73 + "\n"
    cambios_ordenados = sorted(cambios, key=lambda x: x[0])
    for id_prod, nombre, antes, despues in cambios_ordenados:
        nombre_fmt = (nombre[:32] + '...') if len(nombre) > 35 else nombre
        texto += f"{id_prod:<4} {nombre_fmt:<35} {f'${antes:.2f}':>15} {f'${despues:.2f}':>15}\n"
    texto += "-" * 73 + "\n"

    print(texto)
    if input("¿Guardar como PDF? (s/n): ").lower() == 's':
        nombre = input("Nombre de archivo (sin extensión): ")
        guardar_comprobante_pdf(texto, f"{nombre}.pdf", margen_izq=30, margen_sup=60, interlineado=18)