CREATE DATABASE inventario;

USE inventario;


CREATE TABLE categorias(
    id_categoria INT NOT NULL AUTO_INCREMENT UNIQUE,
    nombre VARCHAR(30) NOT NULL,
    descripcion VARCHAR(100) NOT NULL,
    PRIMARY KEY(id_categoria)
);


CREATE TABLE origen(
    id_origen INT NOT NULL AUTO_INCREMENT UNIQUE,
    nombre VARCHAR(30) NOT NULL,
    direccion VARCHAR(100) NOT NULL,
    PRIMARY KEY(id_origen)
);



CREATE TABLE productos(
    id_producto INT NOT NULL AUTO_INCREMENT UNIQUE,
    nombre VARCHAR(30) NOT NULL,
    cantidad INT NOT NULL,
    descripcion VARCHAR(100) NOT NULL,
    id_categoria INT NOT NULL,
    id_origen INT NOT NULL,
    PRIMARY KEY(id_producto),
    FOREIGN KEY(id_categoria) REFERENCES categorias(id_categoria),
    FOREIGN KEY(id_origen) REFERENCES origen(id_origen)
);


