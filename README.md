![Python](https://img.shields.io/badge/Python-3.12-blue)
![MariaDB](https://img.shields.io/badge/MariaDB-DB-lightgrey)
![HeidiSQL](https://img.shields.io/badge/HeidiSQL-GUI-purple)
![ReportLab](https://img.shields.io/badge/ReportLab-PDF_Gen-orange)
![License](https://img.shields.io/badge/License-MIT-green)

# 📦 Sistema de Gestión de Proveedores y Control de Stock

Este es un sistema integral desarrollado en **Python** y **MariaDB** diseñado para automatizar 
la administración de suministros, precios y proveedores. El proyecto nació de la necesidad de
centralizar la información operativa y facilitar la toma de decisiones basada en datos reales de stock.

### Funcionalidades
* **Gestión de Proveedores:** Alta, baja y modificación de datos de contacto.
* **Control de Stock Dinámico:** Seguimiento en tiempo real de productos y existencias.
* **Arquitectura Modular:** Código organizado en módulos específicos para facilitar la escalabilidad.
* **Generación de Reportes:** Creación automática de comprobantes en formato **PDF** para registros administrativos.
<p align="center">
  <img src="img/ipc_2.0.png" width="60%">
</p>


### Tecnologías y Herramientas
* **Lenguaje:** Python 3.12
* **Librerías principales:** 
	* `mariadb`: Conector oficial para integración de BD.
    * `reportlab`: Generación y diseño de documentos PDF.
    * `python-dotenv`: Manejo seguro de variables de entorno.
* **Base de Datos:** MariaDB (Gestionada con HeidiSQL)
* **Diseño de Base de Datos:**
![Estructura SQL](img/proveedores_sql.png)

Se implementó un esquema relacional con integridad referencial, utilizando AUTO_INCREMENT para claves 
primarias y restricciones NOT NULL en campos críticos para asegurar la calidad del dato.   
    
### Instalación

1. Clonar el repositorio:
   `git clone https:github.com/enzoSS01/gestion-proveedores-python`

2. Instalar dependencias:
   `pip install mariadb reportlab python-dotenv`

3. Configuración de Base de Datos:
   * Importar el archivo database_setup.sql en HeidiSQL para crear automáticamente las tablas y cargar los datos iniciales.
   * Configurar las credenciales en el archivo correspondiente (se recomienda el uso de variables de entorno).
   
### 🖼️ Vista Previa del Sistema

**Menú Principal e Interfaz:**

![Menú Principal](img/menu_principal.png)

**Gestión de Datos y Reportes:**
![Listado de Productos](img/lista_productos.png)

*(Captura del sistema interactuando con la base de datos MariaDB)*
