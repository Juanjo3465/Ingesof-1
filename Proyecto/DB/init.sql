-- =====================================================
-- CREACIÓN DE BASE DE DATOS MyBuildingApp
-- =====================================================
CREATE DATABASE MyBuildingApp;
USE MyBuildingApp;

-- =====================================================
-- TABLA: Conjunto
-- =====================================================
CREATE TABLE Conjunto (
    id_conjunto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    direccion VARCHAR(150),
    n_torres INT,
    n_apartamentos INT,
    n_parqueaderos INT,
    reglamento_propiedad_horizontal TEXT,
    estatutos TEXT,
    manual_convivencia TEXT,
    estado_financiero LONGBLOB
);

-- =====================================================
-- TABLA: Apartamentos
-- =====================================================
CREATE TABLE Apartamentos (
    id_apartamento INT AUTO_INCREMENT PRIMARY KEY,
    interior INT,
    torre INT,
    numero INT,
    id_propietario INT,
    n_habitaciones INT,
    n_baños INT,
    area_total FLOAT,
    clasificacion VARCHAR(50),
    deposito BOOLEAN,
    parqueadero BOOLEAN
);

-- =====================================================
-- TABLA: Usuario
-- =====================================================
CREATE TABLE Usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    cedula INT UNIQUE,
    nombre VARCHAR(100),
    fecha_nacimiento DATE,
    correo VARCHAR(120),
    contraseña VARCHAR(100),
    celular INT,
    rol VARCHAR(50)
);

-- =====================================================
-- TABLA: Residente
-- =====================================================
CREATE TABLE Residente (
    id_usuario INT,
    id_apartamento INT,
    PRIMARY KEY (id_usuario, id_apartamento),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_apartamento) REFERENCES Apartamentos(id_apartamento)
);

-- =====================================================
-- TABLA: Zona_comun
-- =====================================================
CREATE TABLE Zona_comun (
    id_zona_comun INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    horario VARCHAR(100),
    capacidad INT,
    reservacion BOOLEAN,
    costo FLOAT,
    imagen LONGBLOB,
    reglamento_uso TEXT
);

-- =====================================================
-- TABLA: Reserva
-- =====================================================
CREATE TABLE Reserva (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_zona_comun INT,
    id_usuario INT,
    fecha_hora DATETIME,
    duracion INT,
    costo INT,
    FOREIGN KEY (id_zona_comun) REFERENCES Zona_comun(id_zona_comun),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

-- =====================================================
-- TABLA: Publicacion
-- =====================================================
CREATE TABLE Publicacion (
    id_publicacion INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    titulo VARCHAR(150),
    fecha_publicacion DATE,
    descripcion TEXT,
    categoria VARCHAR(50),
    visibilidad BOOLEAN,
    estado BOOLEAN,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

-- =====================================================
-- TABLA: Documento_Publicacion
-- =====================================================
CREATE TABLE Documento_Publicacion (
    id_publicacion INT,
    id_documento INT AUTO_INCREMENT,
    nombre VARCHAR(100),
    extension VARCHAR(10),
    documento LONGBLOB,
    PRIMARY KEY (id_documento, id_publicacion),
    FOREIGN KEY (id_publicacion) REFERENCES Publicacion(id_publicacion)
);

-- =====================================================
-- TABLA: Mensaje
-- =====================================================
CREATE TABLE Mensaje (
    id_mensaje INT AUTO_INCREMENT PRIMARY KEY,
    categoria VARCHAR(50),
    asunto VARCHAR(100),
    descripcion TEXT,
    fecha_hora DATETIME,
    conversacion VARCHAR(200)
);

-- =====================================================
-- TABLA: Documento_Mensaje
-- =====================================================
CREATE TABLE Documento_Mensaje (
    id_mensaje INT,
    id_documento INT AUTO_INCREMENT,
    extension VARCHAR(10),
    documento LONGBLOB,
    PRIMARY KEY (id_documento, id_mensaje),
    FOREIGN KEY (id_mensaje) REFERENCES Mensaje(id_mensaje)
);

-- =====================================================
-- TABLA: Usuario_Mensaje
-- =====================================================
CREATE TABLE Usuario_Mensaje (
    id_usuario INT,
    id_mensaje INT,
    papel VARCHAR(50),
    destacado BOOLEAN,
    PRIMARY KEY (id_usuario, id_mensaje),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_mensaje) REFERENCES Mensaje(id_mensaje)
);

-- =====================================================
-- TABLA: Reporte
-- =====================================================
CREATE TABLE Reporte (
    id_usuario INT,
    id_mensaje INT,
    motivo VARCHAR(150),
    comentario TEXT,
    PRIMARY KEY (id_usuario, id_mensaje),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_mensaje) REFERENCES Mensaje(id_mensaje)
);

-- =====================================================
-- TABLA: Asamblea
-- =====================================================
CREATE TABLE Asamblea (
    id_asamblea INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    fecha_hora DATETIME,
    lugar VARCHAR(100),
    descripcion TEXT,
    doc_convocatoria LONGBLOB,
    doc_citacion LONGBLOB,
    acta_asamblea LONGBLOB
);

-- =====================================================
-- TABLA: Delegado
-- =====================================================
CREATE TABLE Delegado (
    id_propietario INT,
    id_asamblea INT,
    nombre VARCHAR(100),
    PRIMARY KEY (id_propietario, id_asamblea),
    FOREIGN KEY (id_propietario) REFERENCES Apartamentos(id_propietario),
    FOREIGN KEY (id_asamblea) REFERENCES Asamblea(id_asamblea)
);

-- =====================================================
-- TABLA: Peticion
-- =====================================================
CREATE TABLE Peticion (
    id_peticion INT AUTO_INCREMENT PRIMARY KEY,
    id_asamblea INT,
    id_propietario INT,
    asunto VARCHAR(100),
    descripcion TEXT,
    FOREIGN KEY (id_asamblea) REFERENCES Asamblea(id_asamblea),
    FOREIGN KEY (id_propietario) REFERENCES Apartamentos(id_propietario)
);
