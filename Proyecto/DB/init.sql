-- =====================================================
-- CREACIÓN DE BASE DE DATOS MyBuildingApp
-- =====================================================
CREATE DATABASE IF NOT EXISTS MyBuildingApp;
USE MyBuildingApp;

-- =====================================================
-- TABLA: Conjunto
-- =====================================================
CREATE TABLE IF NOT EXISTS Conjunto (
    id_conjunto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(150) NOT NULL,
    n_torres INT NOT NULL DEFAULT 0,
    n_apartamentos INT NOT NULL DEFAULT 0,
    n_parqueaderos INT NOT NULL DEFAULT 0,
    reglamento_propiedad_horizontal TEXT,
    estatutos TEXT,
    manual_convivencia TEXT,
    estado_financiero LONGBLOB
);

-- =====================================================
-- TABLA: Usuario
-- =====================================================
CREATE TABLE IF NOT EXISTS Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    cedula INT UNSIGNED UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    correo VARCHAR(120) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    celular VARCHAR(15),
    rol ENUM('Admin','Propietario','Residente') NOT NULL,
    INDEX idx_cedula (cedula),
    INDEX idx_correo (correo)
);

-- =====================================================
-- TABLA: Apartamentos
-- =====================================================
CREATE TABLE IF NOT EXISTS Apartamentos (
    id_apartamento INT AUTO_INCREMENT PRIMARY KEY,
    interior INT,
    torre INT NOT NULL,
    numero INT NOT NULL,
    id_propietario INT,
    n_habitaciones INT NOT NULL DEFAULT 0,
    n_banos INT NOT NULL DEFAULT 0,
    area_total DECIMAL(10,2) NOT NULL,
    clasificacion VARCHAR(50),
    deposito BOOLEAN DEFAULT FALSE,
    parqueadero BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_propietario) REFERENCES Usuario(id_usuario) ON DELETE SET NULL,
    UNIQUE KEY unique_apartment (torre, numero),
    INDEX idx_propietario (id_propietario)
);

-- =====================================================
-- TABLA: Residente
-- =====================================================
CREATE TABLE IF NOT EXISTS Residente (
    id_usuario INT,
    id_apartamento INT,
    fecha_inicio DATE,
    PRIMARY KEY (id_usuario, id_apartamento),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_apartamento) REFERENCES Apartamentos(id_apartamento) ON DELETE CASCADE
);

-- =====================================================
-- TABLA: Zona_comun
-- =====================================================
CREATE TABLE IF NOT EXISTS Zona_comun (
    id_zona_comun INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    horario VARCHAR(100),
    capacidad INT DEFAULT 0,
    reservacion BOOLEAN DEFAULT FALSE,
    costo DECIMAL(10,2) DEFAULT 0.00,
    imagen LONGBLOB,
    reglamento_uso TEXT
);

-- =====================================================
-- TABLA: Reserva
-- =====================================================
CREATE TABLE IF NOT EXISTS Reserva (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_zona_comun INT NOT NULL,
    id_usuario INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    duracion INT NOT NULL,
    costo DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    estado VARCHAR(20) DEFAULT 'Pendiente',
    FOREIGN KEY (id_zona_comun) REFERENCES Zona_comun(id_zona_comun) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    INDEX idx_fecha_hora (fecha_hora),
    INDEX idx_zona (id_zona_comun)
);

-- =====================================================
-- TABLA: Publicacion
-- =====================================================
CREATE TABLE IF NOT EXISTS Publicacion (
    id_publicacion INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    fecha_publicacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    descripcion TEXT,
    categoria VARCHAR(50),
    visibilidad BOOLEAN DEFAULT TRUE,
    estado BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    INDEX idx_fecha (fecha_publicacion),
    INDEX idx_categoria (categoria)
);

-- =====================================================
-- TABLA: Documento_Publicacion
-- =====================================================
CREATE TABLE IF NOT EXISTS Documento_Publicacion (
    id_documento INT AUTO_INCREMENT,
    id_publicacion INT,
    nombre VARCHAR(100) NOT NULL,
    extension VARCHAR(10) NOT NULL,
    documento LONGBLOB NOT NULL,
    fecha_subida DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_documento, id_publicacion),
    FOREIGN KEY (id_publicacion) REFERENCES Publicacion(id_publicacion) ON DELETE CASCADE
);

-- =====================================================
-- TABLA: Mensaje
-- =====================================================
CREATE TABLE IF NOT EXISTS Mensaje (
    id_mensaje INT AUTO_INCREMENT PRIMARY KEY,
    categoria VARCHAR(50),
    asunto VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    conversacion VARCHAR(200),
    INDEX idx_fecha (fecha_hora)
);

-- =====================================================
-- TABLA: Documento_Mensaje
-- =====================================================
CREATE TABLE IF NOT EXISTS Documento_Mensaje (
    id_documento INT AUTO_INCREMENT,
    id_mensaje INT,
    nombre VARCHAR(100),
    extension VARCHAR(10) NOT NULL,
    documento LONGBLOB NOT NULL,
    PRIMARY KEY (id_documento, id_mensaje),
    FOREIGN KEY (id_mensaje) REFERENCES Mensaje(id_mensaje) ON DELETE CASCADE
);

-- =====================================================
-- TABLA: Usuario_Mensaje
-- =====================================================
CREATE TABLE IF NOT EXISTS Usuario_Mensaje (
    id_usuario INT,
    id_mensaje INT,
    papel VARCHAR(50) NOT NULL,
    destacado BOOLEAN DEFAULT FALSE,
    leido BOOLEAN DEFAULT FALSE,
    fecha_lectura DATETIME,
    PRIMARY KEY (id_usuario, id_mensaje),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_mensaje) REFERENCES Mensaje(id_mensaje) ON DELETE CASCADE
);

-- =====================================================
-- TABLA: Reporte
-- =====================================================
CREATE TABLE IF NOT EXISTS Reporte (
    id_usuario INT,
    id_mensaje INT,
    motivo VARCHAR(150) NOT NULL,
    comentario TEXT,
    fecha_reporte DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_usuario, id_mensaje),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_mensaje) REFERENCES Mensaje(id_mensaje) ON DELETE CASCADE
);

-- =====================================================
-- TABLA: Asamblea
-- =====================================================
CREATE TABLE IF NOT EXISTS Asamblea (
    id_asamblea INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_hora DATETIME NOT NULL,
    lugar VARCHAR(100),
    descripcion TEXT,
    doc_convocatoria LONGBLOB,
    doc_citacion LONGBLOB,
    acta_asamblea LONGBLOB,
    estado VARCHAR(20) DEFAULT 'Programada',
    INDEX idx_fecha (fecha_hora)
);

-- =====================================================
-- TABLA: Delegado
-- =====================================================
CREATE TABLE IF NOT EXISTS Delegado (
    id_propietario INT,
    id_asamblea INT,
    nombre VARCHAR(100) NOT NULL,
    PRIMARY KEY (id_propietario, id_asamblea),
    FOREIGN KEY (id_propietario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_asamblea) REFERENCES Asamblea(id_asamblea) ON DELETE CASCADE
);

-- =====================================================
-- TABLA: Peticion
-- =====================================================
CREATE TABLE IF NOT EXISTS Peticion (
    id_peticion INT AUTO_INCREMENT PRIMARY KEY,
    id_asamblea INT NOT NULL,
    id_propietario INT NOT NULL,
    asunto VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_peticion DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'Pendiente',
    FOREIGN KEY (id_asamblea) REFERENCES Asamblea(id_asamblea) ON DELETE CASCADE,
    FOREIGN KEY (id_propietario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE
);
