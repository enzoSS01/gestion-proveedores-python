# mod2_muestra_tablas.py
def mostrar_tablas(conexion):
    try:
        cursor = conexion.cursor()

        # Obtener nombres de todas las tablas
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'control_proveedores'")
        tablas = [fila[0] for fila in cursor.fetchall()]

        if not tablas:
            print("📭 No hay tablas en la base de datos.")
            return

        print("\n📚 Tablas en la base de datos:")
        for nombre in tablas:
            print(f"🔸 {nombre}")

        print("\n📄 Contenido de cada tabla:")
        for nombre in tablas:
            print(f"\n🧾 Tabla: {nombre}")

            # Obtener columnas
            cursor.execute(f"DESCRIBE {nombre}")
            columnas_info = cursor.fetchall()
            columnas = [col[0] for col in columnas_info]

            # Obtener filas
            cursor.execute(f"SELECT * FROM {nombre}")
            filas = cursor.fetchall()

            if not filas:
                print("📭 (Vacía)")
                continue

            # Calcular ancho máximo por columna
            anchos = []
            for i, col in enumerate(columnas):
                max_len = len(col)
                for fila in filas:
                    valor = str(fila[i]) if fila[i] is not None else ""
                    max_len = max(max_len, len(valor))
                anchos.append(max_len + 2)  # margen extra

            # Imprimir encabezado
            print("-" * (sum(anchos) + len(anchos) * 3))
            encabezado = " | ".join(f"{col:<{anchos[i]}}" for i, col in enumerate(columnas))
            print(encabezado)
            print("-" * (sum(anchos) + len(anchos) * 3))

            # Imprimir filas
            for fila in filas:
                fila_formateada = " | ".join(
                    f"{str(valor) if valor is not None else '':<{anchos[i]}}" for i, valor in enumerate(fila)
                )
                print(fila_formateada)

            print("-" * (sum(anchos) + len(anchos) * 3))

    except Exception as e:
        print(f"❌ Error al mostrar tablas: {e}")