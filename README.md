# Proyecto desarrollo de software

“Nuestro proyecto es una aplicación web que permite a los clientes de un restaurante hacer pedidos escaneando un código QR en la mesa. Esto agiliza el proceso, reduce errores y permite dividir cuentas fácilmente, mientras que el restaurante puede gestionar pedidos en tiempo real.”


## Base de datos del proyecto:

```mermaid
erDiagram

    ROLES {
        INT id_rol PK
        VARCHAR nombre
    }

    USUARIOS {
        INT id_usuario PK
        VARCHAR nombre
        VARCHAR correo
        VARCHAR contrasena
        INT id_rol FK
    }

    MESAS {
        INT id_mesa PK
        INT numero_mesa
        VARCHAR estado
    }

    CLIENTES_MESA {
        INT id_cliente_mesa PK
        VARCHAR nombre
        INT id_mesa FK
    }

    CATEGORIAS {
        INT id_categoria PK
        VARCHAR nombre
    }

    PRODUCTOS {
        INT id_producto PK
        VARCHAR nombre
        TEXT descripcion
        NUMERIC precio
        BOOLEAN disponible
        TEXT imagen_url
        INT id_categoria FK
    }

    PEDIDOS {
        INT id_pedido PK
        INT id_mesa FK
        INT id_cliente_mesa FK
        INT id_usuario FK
        VARCHAR tipo_pedido
        VARCHAR estado
        TIMESTAMP fecha
    }

    DETALLE_PEDIDO {
        INT id_detalle PK
        INT id_pedido FK
        INT id_producto FK
        INT cantidad
        NUMERIC precio_unitario
        NUMERIC subtotal
    }

    ROLES ||--o{ USUARIOS : tiene

    USUARIOS ||--o{ PEDIDOS : gestiona

    MESAS ||--o{ CLIENTES_MESA : contiene

    MESAS ||--o{ PEDIDOS : genera

    CLIENTES_MESA ||--o{ PEDIDOS : realiza

    CATEGORIAS ||--o{ PRODUCTOS : clasifica

    PEDIDOS ||--o{ DETALLE_PEDIDO : contiene

    PRODUCTOS ||--o{ DETALLE_PEDIDO : pertenece
```
