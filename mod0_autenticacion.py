import msvcrt

def pedir_contrasena_con_asteriscos(prompt="🔑 Contraseña: "):
    print(prompt, end='', flush=True)
    contrasena = ""
    while True:
        char = msvcrt.getch()
        if char in {b'\r', b'\n'}:  # Enter
            print()
            break
        elif char == b'\x08':  # Backspace
            if len(contrasena) > 0:
                contrasena = contrasena[:-1]
                print('\b \b', end='', flush=True)
        elif char == b'\x03':  # Ctrl+C
            raise KeyboardInterrupt
        else:
            contrasena += char.decode('utf-8')
            print('*', end='', flush=True)
    return contrasena

def login():
    usuarios = {
        "admin": {"clave": "PASSWORD", "rol": "admin"},
        "operador": {"clave": "PASSWORD", "rol": "consulta"}
    }
# Por seguridad, la contraseña se maneja localmente

    intentos = 0
    max_intentos = 3

    while intentos < max_intentos:
        usuario = input("👤 Usuario: ").strip().lower()
        clave = pedir_contrasena_con_asteriscos()

        if usuario in usuarios and usuarios[usuario]["clave"] == clave:
            rol = usuarios[usuario]["rol"]
            print(f"\n✅ Bienvenido, {usuario} ({rol})")
            return {"usuario": usuario, "rol": rol}
        else:
            intentos += 1
            print(f"\n❌ Credenciales inválidas. Intento {intentos}/{max_intentos}")

    print("\n🚫 Se superó el número máximo de intentos. Intente más tarde.")
    return None
