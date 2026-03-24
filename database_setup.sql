-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         12.2.2-MariaDB - MariaDB Server
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.14.0.7165
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para control_proveedores
DROP DATABASE IF EXISTS `control_proveedores`;
CREATE DATABASE IF NOT EXISTS `control_proveedores` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci */;
USE `control_proveedores`;

-- Volcando estructura para tabla control_proveedores.precios
DROP TABLE IF EXISTS `precios`;
CREATE TABLE IF NOT EXISTS `precios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_producto` int(11) NOT NULL,
  `id_proveedor` int(11) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `fecha_actualizacion` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `fk_precios_producto` (`id_producto`),
  KEY `fk_precios_proveedor` (`id_proveedor`),
  CONSTRAINT `fk_precios_producto` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_precios_proveedor` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla control_proveedores.precios: ~27 rows (aproximadamente)
INSERT INTO `precios` (`id`, `id_producto`, `id_proveedor`, `precio`, `fecha_actualizacion`) VALUES
	(4, 4, 1, 8541.58, '2025-10-28 22:43:17'),
	(5, 5, 1, 4880.88, '2025-10-28 22:43:17'),
	(6, 6, 2, 5956.56, '2025-10-28 22:43:17'),
	(7, 7, 2, 8562.55, '2025-10-28 22:43:17'),
	(8, 8, 2, 6514.98, '2025-10-28 22:43:17'),
	(9, 9, 2, 7445.70, '2025-10-28 22:43:17'),
	(10, 10, 2, 4653.60, '2025-10-28 22:43:17'),
	(11, 11, 3, 6872.10, '2025-10-28 22:43:17'),
	(12, 12, 3, 9975.65, '2025-10-28 22:43:17'),
	(13, 13, 3, 2656.28, '2025-10-28 22:43:17'),
	(14, 14, 3, 8645.58, '2025-10-28 22:43:17'),
	(15, 15, 3, 5763.69, '2025-10-28 22:43:17'),
	(18, 18, 4, 6286.01, '2025-10-28 22:43:17'),
	(19, 19, 4, 7492.05, '2025-10-28 22:43:17'),
	(20, 20, 4, 4677.98, '2025-10-28 22:43:17'),
	(21, 21, 5, 2535.03, '2025-10-28 22:43:17'),
	(22, 22, 5, 8758.40, '2025-10-28 22:43:17'),
	(23, 23, 5, 6634.03, '2025-10-28 22:43:17'),
	(24, 24, 5, 3168.77, '2025-10-28 22:43:17'),
	(25, 25, 5, 5031.41, '2025-10-28 22:43:17'),
	(26, 12, 1, 1661.54, '2025-10-31 22:09:05'),
	(27, 6, 1, 7814.83, '2025-10-31 22:30:22'),
	(29, 7, 1, 8.30, '2025-10-31 22:46:47'),
	(31, 12, 5, 67.97, '2025-10-31 23:46:42'),
	(33, 29, 2, 1836.67, '2025-11-02 00:07:28'),
	(36, 32, 2, 3061.11, '2025-11-02 01:45:39'),
	(37, 33, 1, 240.09, '2025-11-02 01:54:51');

-- Volcando estructura para tabla control_proveedores.productos
DROP TABLE IF EXISTS `productos`;
CREATE TABLE IF NOT EXISTS `productos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(200) DEFAULT NULL,
  `categoria` varchar(100) DEFAULT NULL,
  `proveedor_id` int(11) NOT NULL,
  `stock` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `fk_productos_proveedor` (`proveedor_id`),
  CONSTRAINT `fk_productos_proveedor` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedores` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla control_proveedores.productos: ~23 rows (aproximadamente)
INSERT INTO `productos` (`id`, `nombre`, `descripcion`, `categoria`, `proveedor_id`, `stock`) VALUES
	(4, 'Chocolatina', 'Barra de chocolate 50g', 'Dulces', 1, 0),
	(5, 'Agua Mineral', 'Botella 500ml', 'Bebidas', 1, 0),
	(6, 'Pan Integral', 'Paquete 400g', 'Alimentos', 2, 0),
	(7, 'Jugo de Manzana', 'Botella 1L', 'Bebidas', 2, 0),
	(8, 'Galletitas Saladas', 'Paquete 200g', 'Snacks', 2, 0),
	(9, 'Chocolate Negro', 'Barra 50g', 'Dulces', 2, 0),
	(10, 'Agua Saborizada', 'Botella 500ml', 'Bebidas', 2, 0),
	(11, 'Arroz', 'Bolsa 1kg', 'Alimentos', 3, 0),
	(12, 'Lavandina', 'Botella 1L', 'Bebidas', 1, 78),
	(13, 'Sanck max', 'Bolsa 200g', 'Alimentos', 3, 20),
	(14, 'Dulce de Leche', 'Frasco 300g', 'Dulces', 3, 0),
	(15, 'Agua Mineral', 'Botella 1L', 'Bebidas', 3, 0),
	(18, 'Papas Chips', 'Bolsa 150g', 'Snacks', 4, 0),
	(19, 'Caramelos', 'Paquete 100g', 'Dulces', 4, 0),
	(20, 'Agua Con Gas', 'Botella 500ml', 'Bebidas', 4, 0),
	(21, 'Fideos', 'Paquete 500g', 'Alimentos', 5, 32),
	(22, 'Jugo Manzana', 'Botella 1L', 'Bebidas', 5, 0),
	(23, 'Snack de Maíz', 'Bolsa 150g', 'Snacks', 5, 0),
	(24, 'Chocolate con leche extra dulce', 'Barra 1kg', 'Dulces', 5, 15),
	(25, 'Agua Mineral', 'Botella 500ml', 'Bebidas', 5, 0),
	(29, 'Pan rallado', 'Paquete de 200g', 'Alimentos', 2, 9),
	(32, 'Alfajor', 'cajax20', 'Alimentos', 2, 5),
	(33, 'Te', 'caja saquitos', 'Alimentos', 1, 25);

-- Volcando estructura para tabla control_proveedores.proveedores
DROP TABLE IF EXISTS `proveedores`;
CREATE TABLE IF NOT EXISTS `proveedores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `direccion` varchar(150) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla control_proveedores.proveedores: ~6 rows (aproximadamente)
INSERT INTO `proveedores` (`id`, `nombre`, `direccion`, `telefono`, `email`) VALUES
	(1, 'Proveedor K', 'Av. Libertad 123', '11-2515-4585', 'contacto@proveedora.com'),
	(2, 'Proveedor X', 'Calle sol 584', '222-354-5485', 'ventas@yahoo.com.ar'),
	(3, 'Proveedor C', 'Ruta 8 Km 32', '333-444-5555', 'info@proveedorc.com'),
	(4, 'Proveedor D', 'San Martín 789', '444-555-6666', 'admin@proveedord.com'),
	(5, 'Proveedor E', 'Belgrano 101', '555-666-7777', 'soporte@proveedore.com'),
	(8, 'Proveedor M', 'Av Cordoba 5568', '46981587', 'proveedorF@hotmail.com');

-- Volcando estructura para tabla control_proveedores.usuarios
DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_usuario` varchar(50) DEFAULT NULL,
  `contrasena` varchar(255) DEFAULT NULL,
  `rol` enum('admin','consulta') DEFAULT 'consulta',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `nombre_usuario` (`nombre_usuario`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Volcando datos para la tabla control_proveedores.usuarios: ~0 rows (aproximadamente)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
