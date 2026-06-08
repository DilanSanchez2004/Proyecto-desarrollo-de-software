from app.config.db import get_connection
from psycopg2.extras import RealDictCursor

def generar_factura(id_mesa):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT numero_mesa FROM mesas WHERE id_mesa = %s
            """, (id_mesa,))
            mesa = cur.fetchone()
            if not mesa:
                return None

            cur.execute("""
                SELECT DISTINCT p.id_cliente_mesa, cm.nombre AS cliente
                FROM pedidos p
                LEFT JOIN clientes_mesa cm ON p.id_cliente_mesa = cm.id_cliente_mesa
                WHERE p.id_mesa = %s AND p.estado = 'entregado' AND p.id_factura IS NULL
                ORDER BY p.id_cliente_mesa
            """, (id_mesa,))
            clientes = cur.fetchall()

            if not clientes:
                return None

            import json
            primer_id = None

            for cliente in clientes:
                id_cliente_mesa = cliente["id_cliente_mesa"]
                nombre_cliente = cliente["cliente"] or "Anónimo"

                cur.execute("""
                    SELECT id_pedido FROM pedidos
                    WHERE id_mesa = %s AND id_cliente_mesa = %s
                      AND estado = 'entregado' AND id_factura IS NULL
                    ORDER BY fecha
                """, (id_mesa, id_cliente_mesa))
                pedidos = cur.fetchall()
                if not pedidos:
                    continue

                id_pedidos = [p["id_pedido"] for p in pedidos]

                items = []
                total = 0
                for id_pedido in id_pedidos:
                    cur.execute("""
                        SELECT dp.id_producto, pr.nombre, dp.cantidad, dp.precio_unitario, dp.subtotal
                        FROM detalle_pedido dp
                        JOIN productos pr ON dp.id_producto = pr.id_producto
                        WHERE dp.id_pedido = %s
                    """, (id_pedido,))
                    for item in cur.fetchall():
                        items.append({
                            "id_producto": item["id_producto"],
                            "nombre": item["nombre"],
                            "cantidad": item["cantidad"],
                            "precio_unitario": float(item["precio_unitario"]),
                            "subtotal": float(item["subtotal"]),
                        })
                        total += float(item["subtotal"])

                items_json = json.dumps(items, ensure_ascii=False)

                cur.execute("""
                    INSERT INTO facturas (id_mesa, numero_mesa, nombre_cliente, total, items)
                    VALUES (%s, %s, %s, %s, %s::jsonb)
                    RETURNING id_factura
                """, (id_mesa, mesa["numero_mesa"], nombre_cliente, round(total, 2), items_json))
                id_factura = cur.fetchone()["id_factura"]

                cur.execute("""
                    UPDATE pedidos SET id_factura = %s WHERE id_pedido = ANY(%s)
                """, (id_factura, id_pedidos))

                if primer_id is None:
                    primer_id = id_factura

        conn.commit()
    return primer_id

def obtener_facturas():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT f.id_factura, f.numero_mesa, f.nombre_cliente,
                       f.fecha_emision, f.total
                FROM facturas f
                ORDER BY f.fecha_emision DESC
            """)
            return cur.fetchall()

def obtener_factura_por_id(id_factura):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT f.id_factura, f.id_mesa, f.numero_mesa, f.nombre_cliente,
                       f.fecha_emision, f.total, f.items
                FROM facturas f
                WHERE f.id_factura = %s
            """, (id_factura,))
            row = cur.fetchone()
            if row and isinstance(row.get("items"), str):
                import json
                row["items"] = json.loads(row["items"])
            return row

def contar_facturas_hoy():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT COUNT(*) AS total,
                       COALESCE(SUM(total), 0) AS total_ingresos
                FROM facturas
                WHERE fecha_emision::date = CURRENT_DATE
            """)
            return cur.fetchone()

def contar_facturas_totales():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT COUNT(*) AS total FROM facturas")
            return cur.fetchone()
