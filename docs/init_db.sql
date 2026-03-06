-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 06-03-2026 a las 10:04:20
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;


-- Base de datos: consultasmedicas
-- Tabla: consultas_medicas
-- =====================================================

-- 1) Crear base de datos
DROP DATABASE IF EXISTS consultasmedicas;
CREATE DATABASE IF NOT EXISTS consultasmedicas
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- 2) Usar la base de datos
USE consultasmedicas;
-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `consultas_medicas`
--

CREATE TABLE `consultas_medicas` (
  `id` int(11) NOT NULL,
  `paciente_nombre` varchar(100) NOT NULL,
  `paciente_dni` varchar(9) NOT NULL,
  `medico_nombre` varchar(100) NOT NULL,
  `fecha_consulta` datetime NOT NULL,
  `motivo_consulta` varchar(255) NOT NULL,
  `diagnostico` text DEFAULT NULL,
  `estado` enum('programada','confirmada','realizada','cancelada','no_asistio') NOT NULL DEFAULT 'programada',
  `costo` decimal(8,2) NOT NULL,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `consultas_medicas`
--

INSERT INTO `consultas_medicas` (`id`, `paciente_nombre`, `paciente_dni`, `medico_nombre`, `fecha_consulta`, `motivo_consulta`, `diagnostico`, `estado`, `costo`, `creado_en`) VALUES
(1, 'Juan Pérez', '12345678A', 'Dr. García', '2024-01-15 10:30:00', 'Dolor de cabeza persistente', 'Migraña tensional', 'realizada', 45.00, '2026-03-02 10:56:57'),
(2, 'María López', '87654321B', 'Dr. Martínez', '2024-01-16 14:15:00', 'Dolor abdominal', 'Inflamación estomacal leve', 'realizada', 35.50, '2026-03-02 10:56:57'),
(3, 'Carlos Rodríguez', '98765432C', 'Dr. Fernández', '2024-01-17 11:45:00', 'Dolor de espalda crónico', 'Lumbalgia por mala postura', 'programada', 65.75, '2026-03-02 10:56:57'),
(4, 'Ana Gómez', '43218765D', 'Dr. López', '2024-01-18 09:20:00', 'Fiebre y tos persistente', 'Resfriado común con posible infección respiratoria leve.', 'programada', 38.99, '2026-03-02 10:56:57');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `consultas_medicas`
--
ALTER TABLE `consultas_medicas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `paciente_dni` (`paciente_dni`);
COMMIT;

-- =====================================================
-- Usuario de base de datos para la aplicación consultasmedicas
-- =====================================================

-- Crear usuario (si no existe)
CREATE USER IF NOT EXISTS 'consultasappMaria'@'localhost'
IDENTIFIED BY 'consultasapp123';

-- Otorgar todos los permisos SOLO sobre la base consultasmedicas
GRANT ALL PRIVILEGES ON consultasmedicas.* TO 'consultasappMaria'@'localhost';
-- Aplicar cambios de privilegios
FLUSH PRIVILEGES;
-- SELECT * FROM consultas_medicas;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
