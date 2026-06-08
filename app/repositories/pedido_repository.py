from app.config.db import get_connection
from psycopg2.extras import RealDictCursor

def obtener_pedidos_por_mesa():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT
                    p.id_pedido,
                    p.id_mesa,
                    p.estado AS estado_pedido,
                    p.tipo_pedido,
                    p.fecha,
                    cm.nombre AS cliente,
                    json_agg(
                        json_build_object(
                            'id_producto', dp.id_producto,
                            'nombre', pr.nombre,
                            'cantidad', dp.cantidad,
                            'precio_unitario', dp.precio_unitario,
                            'subtotal', dp.subtotal
                        )
                    ) AS items
                FROM pedidos p
                JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
                JOIN productos pr ON dp.id_producto = pr.id_producto
                LEFT JOIN clientes_mesa cm ON p.id_cliente_mesa = cm.id_cliente_mesa
                WHERE p.estado = 'pendiente'
                GROUP BY p.id_pedido, cm.nombre
                ORDER BY p.fecha DESC
            """)
            rows = cur.fetchall()
            agrupados = {}
            for row in rows:
                id_mesa = row["id_mesa"]
                if id_mesa not in agrupados:
                    agrupados[id_mesa] = []
                agrupados[id_mesa].append(row)
            return agrupados

def entregar_pedido(id_pedido):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE pedidos SET estado = 'entregado' WHERE id_pedido = %s",
                (id_pedido,)
            )
            conn.commit()
            return cur.rowcount > 0

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
