from app.config.db import get_connection

def crear_pedido(id_mesa, id_cliente_mesa, id_usuario, tipo_pedido, items):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO pedidos (id_mesa, id_cliente_mesa, id_usuario,
                                     tipo_pedido, estado, fecha)
                VALUES (%s, %s, %s, %s, 'pendiente', NOW())
                RETURNING id_pedido
            """, (id_mesa, id_cliente_mesa, id_usuario, tipo_pedido))

            id_pedido = cur.fetchone()[0]

            for item in items:
                subtotal = item["cantidad"] * item["precio_unitario"]
                cur.execute("""
                    INSERT INTO detalle_pedido
                        (id_pedido, id_producto, cantidad, precio_unitario, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    id_pedido,
                    item["id_producto"],
                    item["cantidad"],
                    item["precio_unitario"],
                    subtotal
                ))
        conn.commit()
    return id_pedido
