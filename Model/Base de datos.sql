CREATE TABLE RESTAURANTE (
    id_restaurante SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(255),
    telefono VARCHAR(10)
);


CREATE TABLE CATEGORIA (
    id_categoria SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    id_restaurante INT REFERENCES RESTAURANTE(id_restaurante) ON DELETE CASCADE
);


CREATE TABLE MESA (
    id_mesa SERIAL PRIMARY KEY,
    numero INT NOT NULL,
    qr_codigo VARCHAR(255) UNIQUE,
    id_restaurante INT REFERENCES RESTAURANTE(id_restaurante) ON DELETE CASCADE
);

CREATE TABLE PRODUCTO (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    disponible BOOLEAN DEFAULT TRUE,
    id_categoria INT REFERENCES CATEGORIA(id_categoria) ON DELETE SET NULL
);


CREATE TABLE PEDIDO (
    id_pedido SERIAL PRIMARY KEY,
    id_mesa INT REFERENCES MESA(id_mesa) ON DELETE CASCADE,
    estado VARCHAR(20) DEFAULT 'pendiente', -- pendiente, en_preparacion, entregado, pagado
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10, 2) DEFAULT 0.00
);


CREATE TABLE DETALLE_PEDIDO (
    id_detalle SERIAL PRIMARY KEY,
    id_pedido INT REFERENCES PEDIDO(id_pedido) ON DELETE CASCADE,
    id_producto INT REFERENCES PRODUCTO(id_producto),
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10, 2) NOT NULL
);


CREATE TABLE PARTICIPANTE (
    id_participante SERIAL PRIMARY KEY,
    id_pedido INT REFERENCES PEDIDO(id_pedido) ON DELETE CASCADE,
    nombre VARCHAR(100)
);


CREATE TABLE DETALLE_PARTICIPANTE (
    id_detalle_participante SERIAL PRIMARY KEY,
    id_participante INT REFERENCES PARTICIPANTE(id_participante) ON DELETE CASCADE,
    id_detalle INT REFERENCES DETALLE_PEDIDO(id_detalle) ON DELETE CASCADE
);


CREATE TABLE PAGO (
    id_pago SERIAL PRIMARY KEY,
    id_pedido INT REFERENCES PEDIDO(id_pedido) ON DELETE CASCADE,
    monto DECIMAL(10, 2) NOT NULL,
    metodo VARCHAR(30), -- efectivo, tarjeta, transferencia
    estado VARCHAR(20), -- aprobado, pendiente, rechazado
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);