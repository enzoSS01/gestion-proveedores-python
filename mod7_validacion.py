import re
from decimal import Decimal

# -------------------------------
# Validaciones básicas
# -------------------------------

def validar_nombre(nombre):
    # Permite letras, espacios, acentos, ñ, guiones y apóstrofes
    return bool(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s'\-]+$", nombre.strip()))

def validar_telefono(telefono):
    limpio = re.sub(r"[^\d]", "", telefono)
    return 6 <= len(limpio) <= 15

def validar_email(email):
    # Regex más robusta para emails comunes
    return bool(re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email.strip()))

def validar_direccion(direccion):
    return len(direccion.strip()) >= 5  # mínimo 5 caracteres

# -------------------------------
# Confirmaciones y opciones
# -------------------------------

def confirmar_si_no(mensaje, max_intentos=3):
    intentos = 0
    while intentos < max_intentos:
        resp = input(mensaje + " (S/N): ").strip().lower()
        if resp in ('s', 'si', 'sí'):
            return True
        elif resp in ('n', 'no'):
            return False
        else:
            intentos += 1
            print(f"⚠️ Respuesta inválida. Intento {intentos}/{max_intentos}.\n")
            if intentos < max_intentos:
                input("Presione Enter para intentar nuevamente...")

    print("🚫 Se superó el número máximo de intentos. Se asumirá 'No'.\n")
    return False

def pedir_opcion_valida(mensaje, opciones_validas, max_intentos=3):
    intentos = 0
    while intentos < max_intentos:
        opcion = input(mensaje).strip()
        if opcion in opciones_validas:
            return opcion
        print(f"❌ Opción inválida. Las opciones válidas son: {', '.join(opciones_validas)}")
        intentos += 1
        if intentos < max_intentos:
            input("Presione Enter para intentar nuevamente...")

    print("🚫 Se superó el número máximo de intentos. Operación cancelada.")
    input("Presione Enter para continuar...")
    return None

# -------------------------------
# Pedir valores numéricos
# -------------------------------

def pedir_entero_positivo(mensaje, max_intentos=3):
    intentos = 0
    while intentos < max_intentos:
        try:
            valor = int(input(mensaje))
            if valor > 0:
                return valor
            else:
                print(f"⚠️ Debe ingresar un número positivo. Intento {intentos+1}/{max_intentos}.")
        except ValueError:
            print(f"⚠️ Entrada no válida. Debe ser un número entero. Intento {intentos+1}/{max_intentos}.")
        intentos += 1
        if intentos < max_intentos:
            input("Presione Enter para intentar nuevamente...")

    print("🚫 Se superaron los intentos. Volviendo al inicio.")
    input("Presione Enter para continuar...")
    return None

def pedir_valor_numerico_valido(mensaje, tipo=float, condicion=lambda x: True, max_intentos=3):
    intentos = 0
    while intentos < max_intentos:
        entrada = input(mensaje).strip()
        try:
            valor = tipo(entrada)
            if condicion(valor):
                return valor
            else:
                print("❌ Valor fuera de rango o inválido.")
        except Exception:
            print("❌ Entrada inválida. Debe ser un número.")
        intentos += 1
        if intentos < max_intentos:
            input("Presione Enter para intentar nuevamente...")

    print("🚫 Se superaron los intentos. Operación cancelada.")
    input("Presione Enter para continuar...")
    return None

# -------------------------------
# Pedir textos
# -------------------------------

def pedir_texto_no_vacio(mensaje, max_intentos=3, condicion=None, mensaje_error=None):
    intentos = 0
    while intentos < max_intentos:
        texto = input(mensaje).strip()
        if texto.upper() == "CANCELAR":
            return "CANCELAR"
        if not texto:
            print("❌ El texto no puede estar vacío.")
        elif condicion and not condicion(texto):
            print(mensaje_error or "❌ Entrada inválida.")
        else:
            return texto
        intentos += 1
        if intentos < max_intentos:
            input("Presione Enter para intentar nuevamente...")
    print("🚫 Se superaron los intentos. Operación cancelada.")
    input("Presione Enter para continuar...")
    return None

def pedir_texto_opcional(mensaje, valor_actual, condicion=None, mensaje_error=None, max_intentos=3):
    intentos = 0
    while intentos < max_intentos:
        entrada = input(f"{mensaje}[{valor_actual}]: ").strip()
        if entrada == "":
            return valor_actual
        if entrada.upper() == "CANCELAR":
            return "CANCELAR"
        if condicion and not condicion(entrada):
            print(mensaje_error or "❌ Entrada inválida.")
        else:
            return entrada
        intentos += 1
        if intentos < max_intentos:
            input("Presione Enter para intentar nuevamente...")
    print("🚫 Se superaron los intentos. Se mantendrá el valor actual.")
    input("Presione Enter para continuar...")
    return valor_actual

def pedir_entero_opcional(mensaje, valor_actual, max_intentos=3):
    intentos = 0
    while intentos < max_intentos:
        entrada = input(f"{mensaje}[{valor_actual}]: ").strip()
        if entrada == "":
            return valor_actual
        if entrada.upper() == "CANCELAR":
            return "CANCELAR"
        if entrada.isdigit() and int(entrada) >= 0:
            return int(entrada)
        print(f"❌ Ingrese un número entero válido o deje en blanco para mantener el valor actual. Intento {intentos+1}/{max_intentos}")
        intentos += 1
        if intentos < max_intentos:
            input("Presione Enter para intentar nuevamente...")
    print("🚫 Se superaron los intentos. Se mantendrá el valor actual.")
    input("Presione Enter para continuar...")
    return valor_actual