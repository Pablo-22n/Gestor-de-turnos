-- ============================================================
-- schema.sql
-- Base de datos del Sistema de Gestión de Turnos.
-- ============================================================

CREATE DATABASE IF NOT EXISTS turnos
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE turnos;

-- ------------------------------------------------------------
-- Tabla: pacientes
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS pacientes (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    dni         VARCHAR(15)  NOT NULL UNIQUE,
    nombre      VARCHAR(50) NOT NULL,
    apellido    VARCHAR(50) NOT NULL,
    telefono    VARCHAR(30)
);

-- ------------------------------------------------------------
-- Tabla: profesionales
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS profesionales (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    dni             VARCHAR(15)  NOT NULL UNIQUE,
    nombre          VARCHAR(50) NOT NULL,
    apellido        VARCHAR(50) NOT NULL,
    especialidad    VARCHAR(50)
);

-- ------------------------------------------------------------
-- Tabla: turnos
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS turnos (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id     INT      NOT NULL,
    profesional_id  INT      NOT NULL,
    fecha           DATE     NOT NULL,
    hora            TIME     NOT NULL,
    estado          ENUM('pendiente','confirmado','atendido','cancelado','ausente')
                    NOT NULL DEFAULT 'pendiente',

    FOREIGN KEY (paciente_id)    REFERENCES pacientes(id),
    FOREIGN KEY (profesional_id) REFERENCES profesionales(id),
    INDEX ix_turnos_prof_fecha (profesional_id, fecha)
);

-- ------------------------------------------------------------
-- Tabla: usuarios (Para el Login)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(64) NOT NULL,
    rol VARCHAR(20) NOT NULL DEFAULT 'recepcionista'
);

-- Usuario admin por defecto (Usuario: admin / Contraseña: admin123)
INSERT INTO usuarios (usuario, password_hash, rol) 
VALUES ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin');