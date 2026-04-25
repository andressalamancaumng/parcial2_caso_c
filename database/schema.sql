-- Esquema Alcaldia Digital de Municipio X
CREATE DATABASE alcaldia_db;
\c alcaldia_db;

CREATE TABLE ciudadanos (
    id            SERIAL PRIMARY KEY,
    cedula        VARCHAR(12) UNIQUE NOT NULL,
    nombre        VARCHAR(120) NOT NULL,
    email         VARCHAR(255) UNIQUE NOT NULL,
    telefono      VARCHAR(20),
    password_hash VARCHAR(255) NOT NULL,
    role          VARCHAR(30) DEFAULT 'ROLE_CIUDADANO',
    estado        VARCHAR(20) DEFAULT 'activo',
    created_at    TIMESTAMP DEFAULT NOW()
);

CREATE TABLE funcionarios (
    id            SERIAL PRIMARY KEY,
    nombre        VARCHAR(120) NOT NULL,
    email         VARCHAR(255) UNIQUE NOT NULL,
    cargo         VARCHAR(100),
    password_hash VARCHAR(255) NOT NULL,
    role          VARCHAR(30) DEFAULT 'ROLE_FUNCIONARIO',
    estado        VARCHAR(20) DEFAULT 'activo',
    created_at    TIMESTAMP DEFAULT NOW()
);

CREATE TABLE tramites (
    id           SERIAL PRIMARY KEY,
    ciudadano_id INT REFERENCES ciudadanos(id),
    tipo         VARCHAR(80) NOT NULL,
    estado       VARCHAR(30) DEFAULT 'pendiente',
    descripcion  TEXT,
    created_at   TIMESTAMP DEFAULT NOW(),
    updated_at   TIMESTAMP DEFAULT NOW()
);

-- NUNCA almacenar tarjeta/CVV — esta tabla documenta la vulnerabilidad
CREATE TABLE transacciones (
    id           SERIAL PRIMARY KEY,
    ciudadano_id INT REFERENCES ciudadanos(id),
    monto        DECIMAL(12,2),
    matricula    VARCHAR(30),
    tarjeta      VARCHAR(20),  -- ← VULNERABLE: no debe existir este campo
    cvv          VARCHAR(4),   -- ← VULNERABLE: no debe existir este campo
    estado       VARCHAR(20),
    created_at   TIMESTAMP DEFAULT NOW()
);

CREATE USER alcaldia_app WITH PASSWORD 'CHANGE_ME';
GRANT CONNECT ON DATABASE alcaldia_db TO alcaldia_app;
GRANT USAGE ON SCHEMA public TO alcaldia_app;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO alcaldia_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO alcaldia_app;
