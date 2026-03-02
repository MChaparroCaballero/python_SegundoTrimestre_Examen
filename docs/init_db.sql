-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3307
-- Tiempo de generación: 02-03-2026 a las 12:57:06
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- =====================================================
-- Base de datos: ConsultasMedicasApp
-- Tabla: producto
-- =====================================================

-- 1) Crear base de datos
DROP DATABASE IF EXISTS ConsultasMedicasApp;
CREATE DATABASE IF NOT EXISTS ConsultasMedicasApp
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- 2) Usar la base de datos
USE ConsultasMedicasApp;
-- --------------------------------------------------------

-- 3) Crear tabla consultas
CREATE TABLE `consultas` (
  `id` int(11) NOT NULL,
  `paciente_nombre` varchar(100) NOT NULL,
  `paciente_dni` varchar(9) NOT NULL,
  `medico_nombre` varchar(100) NOT NULL,
  `fecha_consulta` datetime NOT NULL,
  `motivo_consulta` varchar(255) NOT NULL,
  `diagnostico` varchar(255) DEFAULT NULL,
  `estado` enum('pendiente','en proceso','finalizada','cancelada') NOT NULL DEFAULT 'pendiente',
  `costo` decimal(10,2) NOT NULL,
  `creado_en` timestamp DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `consultas`
--

INSERT INTO `consultas` (`id`, `paciente_nombre`, `paciente_dni`, `medico_nombre`, `fecha_consulta`, `motivo_consulta`, `diagnostico`, `estado`, `costo`, `creado_en`) VALUES
(1, 'Juan Pérez', '12345678A', 'Dr. García', '2024-01-15 10:30:00', 'Dolor de cabeza persistente', 'Migraña tensional', 'finalizada', 45.00, '2026-03-02 11:56:57'),
(2, 'María López', '87654321B', 'Dr. Martínez', '2024-01-16 14:15:00', 'Dolor abdominal', 'Inflamación estomacal leve', 'finalizada', 35.50, '2026-03-02 11:56:57'),
(3, 'Carlos Rodríguez', '98765432C', 'Dr. Fernández', '2024-01-17 11:45:00', 'Dolor de espalda crónico', 'Lumbalgia por mala postura', '', 65.75, '2026-03-02 11:56:57'),
(4, 'Ana Gómez', '43218765D', 'Dr. López', '2024-01-18 09:20:00', 'Fiebre y tos persistente', 'Resfriado común con posible infección respiratoria leve.', 'pendiente', 38.99, '2026-03-02 11:56:57');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `consultas`
--
ALTER TABLE `consultas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `paciente_dni` (`paciente_dni`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `consultas`
--
ALTER TABLE `consultas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

-- =====================================================
-- Usuario de base de datos para la aplicación ConsultasMedicasApp
-- =====================================================

-- Crear usuario (si no existe)
CREATE USER IF NOT EXISTS 'consultasappMaria'@'localhost'
IDENTIFIED BY 'consultasapp123';

-- Otorgar todos los permisos SOLO sobre la base ConsultasMedicasApp
GRANT ALL PRIVILEGES ON ConsultasMedicasApp.* TO 'consultasappMaria'@'localhost';
-- Aplicar cambios de privilegios
FLUSH PRIVILEGES;
-- SELECT * FROM consultas;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
