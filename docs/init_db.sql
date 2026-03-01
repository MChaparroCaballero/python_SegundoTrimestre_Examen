-- =====================================================
-- Base de datos: ConsultasApp
-- Tabla: producto
-- =====================================================

-- 1) Crear base de datos
DROP DATABASE IF EXISTS ConsultasApp;
CREATE DATABASE IF NOT EXISTS ConsultasApp
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- 2) Usar la base de datos
USE ConsultasApp;

-- 3) Crear tabla producto
CREATE TABLE consulta_medica (
  id INT UNSIGNED AUTO_INCREMENT,
  paciente_nombre VARCHAR(100) NOT NULL,
  paciente_dni VARCHAR(20) NOT NULL,
  medico_nombre VARCHAR(100) NOT NULL,
  fecha_consulta DATETIME NOT NULL,
  motivo_consulta VARCHAR(255) NULL,
  diagnostico VARCHAR(255) NOT NULL,
  estado enum('pendiente', 'en_curso', 'finalizada', 'cancelada') NOT NULL DEFAULT 'pendiente',
  coste DECIMAL(8,2) NOT NULL,
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  

  CONSTRAINT pk_consulta_medica PRIMARY KEY (id),
  Constraint uq_paciente_dni UNIQUE (paciente_dni)
);

-- =====================================================
-- 4) Datos de ejemplo (seed data)
-- =====================================================

INSERT INTO consulta_medica (paciente_nombre, paciente_dni, medico_nombre, fecha_consulta, motivo_consulta, diagnostico, estado, coste) VALUES
('Juan Pérez', '12345678A', 'Dr. García', '2024-01-15 10:30:00', 'Dolor de cabeza persistente', 'Migraña tensional', 'finalizada', 45.00),
('María López', '87654321B', 'Dr. Martínez', '2024-01-16 14:15:00', 'Dolor abdominal', 'Inflamación estomacal leve', 'finalizada', 35.50),
('Carlos Rodríguez', '98765432C', 'Dr. Fernández', '2024-01-17 11:45:00', 'Dolor de espalda crónico', 'Lumbalgia por mala postura', 'en_curso', 65.75),
('Ana Gómez', '43218765D', 'Dr. López', '2024-01-18 09:20:00', 'Fiebre y tos persistente', 'Resfriado común con posible infección respiratoria leve.', 'pendiente', 38.99);

-- =====================================================
-- Usuario de base de datos para la aplicación ConsultasApp
-- =====================================================

-- Crear usuario (si no existe)
CREATE USER IF NOT EXISTS 'consultasappMaria'@'localhost'
IDENTIFIED BY 'consultasapp123';

-- Otorgar todos los permisos SOLO sobre la base ConsultasApp
GRANT ALL PRIVILEGES ON ConsultasApp.* TO 'consultasappMaria'@'localhost';
-- Aplicar cambios de privilegios
FLUSH PRIVILEGES;
-- SELECT * FROM consulta_medica;