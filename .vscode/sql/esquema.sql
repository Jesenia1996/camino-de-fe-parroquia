-- Archivo: sql/esquema.sql
-- Propósito: Crear la estructura de la base de datos relacional para el Proyecto Integrador

-- 1. Crear la base de datos (si no existe) y seleccionarla
CREATE DATABASE IF NOT EXISTS camino_de_fe;
USE camino_de_fe;

-- 2. Crear la tabla de Proveedores (Entidad independiente)
CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(100)
);

-- 3. Crear la tabla de Productos (Entidad dependiente con Clave Foránea)
CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    cantidad INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    id_proveedor INT,
    -- Relación: Un producto pertenece a un proveedor
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor) ON DELETE SET NULL
);

-- 4. Insertar datos de prueba para validar la relación (Opcional pero recomendado)
INSERT INTO proveedores (nombre, telefono, correo) VALUES 
('Librería Católica San Pablo', '0991234567', 'contacto@libreriasanpablo.com'),
('Artículos Litúrgicos Jesús', '0987654321', 'ventas@liturgicajesus.com');

INSERT INTO productos (nombre, categoria, cantidad, precio, id_proveedor) VALUES 
('Manual del Monaguillo', 'Libros', 15, 15.50, 1),
('Alba blanca talla M', 'Vestimenta', 5, 45.00, 2);