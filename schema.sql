-- ============================================================
-- schema.sql
-- Base de datos del Sistema de Gestión de Turnos.
--
-- Este archivo crea la base de datos y sus tablas.
-- Se ejecuta UNA sola vez al configurar el proyecto.

CREATE DATABASE IF NOT EXISTS turnos
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE turnos;


-- ------------------------------------------------------------
-- 2. Tabla: pacientes
-- ------------------------------------------------------------
-- Almacena los datos de las personas que piden turnos.
-- El DNI es único: no puede haber dos pacientes con el mismo.
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS pacientes (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    dni         VARCHAR(15)  NOT NULL UNIQUE,
    nombre      VARCHAR(100) NOT NULL,
    apellido    VARCHAR(100) NOT NULL,
    telefono    VARCHAR(30)
);


-- ------------------------------------------------------------
-- 3. Tabla: profesionales
-- ------------------------------------------------------------
-- Almacena los datos de los médicos o profesionales que
-- atienden los turnos.
-- El DNI también es único.
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS profesionales (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    dni             VARCHAR(15)  NOT NULL UNIQUE,
    nombre          VARCHAR(100) NOT NULL,
    apellido        VARCHAR(100) NOT NULL,
    especialidad    VARCHAR(100)
);


-- ------------------------------------------------------------
-- 4. Tabla: turnos
-- ------------------------------------------------------------
-- Almacena los turnos reservados.
--
-- Cada turno:
--   - pertenece a un paciente (paciente_id)
--   - es atendido por un profesional (profesional_id)
--   - tiene una fecha y una hora
--   - tiene un estado (pendiente, confirmado, atendido, etc.)
--
-- Todos los turnos duran 30 minutos (no se guarda la duración,
-- se asume fija en la lógica de la aplicación).
--
-- El estado puede ser:
--   pendiente  → reservado, sin confirmar
--   confirmado → confirmado por el paciente
--   atendido   → ya fue atendido
--   cancelado  → cancelado (libera el horario)
--   ausente    → el paciente no vino (libera el horario)
--
-- Los estados cancelado y ausente liberan el horario, por eso
-- la búsqueda de conflictos los excluye.
-- ------------------------------------------------------------

CREATE TABLE IF NOT EXISTS turnos (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id     INT      NOT NULL,
    profesional_id  INT      NOT NULL,
    fecha           DATE     NOT NULL,
    hora            TIME     NOT NULL,
    estado          ENUM('pendiente','confirmado','atendido','cancelado','ausente')
                    NOT NULL DEFAULT 'pendiente',

    -- Relaciones con las otras tablas
    FOREIGN KEY (paciente_id)    REFERENCES pacientes(id),
    FOREIGN KEY (profesional_id) REFERENCES profesionales(id),

    -- Índice para acelerar la búsqueda más frecuente:
    -- "turnos de un profesional en una fecha"
    INDEX ix_turnos_prof_fecha (profesional_id, fecha)
);
