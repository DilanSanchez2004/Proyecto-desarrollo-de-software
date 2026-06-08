from app.config.db import get_connection
from psycopg2.extras import RealDictCursor

def contar_mesas():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT
                    COUNT(*) AS total,
                    COALESCE(SUM(CASE WHEN estado = 'libre' THEN 1 ELSE 0 END), 0) AS libres,
                    COALESCE(SUM(CASE WHEN estado = 'ocupada' THEN 1 ELSE 0 END), 0) AS ocupadas
                FROM mesas
            """)
            return cur.fetchone()

def contar_pedidos():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT
                    COALESCE(SUM(CASE WHEN estado = 'pendiente' THEN 1 ELSE 0 END), 0) AS pendientes,
                    COALESCE(SUM(CASE WHEN estado = 'en preparacion' THEN 1 ELSE 0 END), 0) AS en_preparacion,
                    COALESCE(SUM(CASE WHEN estado = 'entregado' THEN 1 ELSE 0 END), 0) AS entregados
                FROM pedidos
                WHERE fecha::date = CURRENT_DATE
            """)
            return cur.fetchone()

def contar_productos():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT
                    COUNT(*) AS total,
                    COALESCE(SUM(CASE WHEN disponible = TRUE THEN 1 ELSE 0 END), 0) AS disponibles,
                    COALESCE(SUM(CASE WHEN disponible = FALSE THEN 1 ELSE 0 END), 0) AS no_disponibles
                FROM productos
            """)
            return cur.fetchone()

def contar_usuarios():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT COUNT(*) AS total
                FROM usuarios u
                JOIN roles r ON u.id_rol = r.id_rol
                WHERE r.nombre = 'admin'
            """)
            return cur.fetchone()

def contar_categorias():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT COUNT(*) AS total FROM categorias")
            return cur.fetchone()

def obtener_ultimos_pedidos(limite=5):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT p.id_pedido, p.estado, p.fecha, m.numero_mesa,
                       COALESCE(cm.nombre, 'Anónimo') AS cliente
                FROM pedidos p
                JOIN mesas m ON p.id_mesa = m.id_mesa
                LEFT JOIN clientes_mesa cm ON p.id_cliente_mesa = cm.id_cliente_mesa
                ORDER BY p.fecha DESC
                LIMIT %s
            """, (limite,))
            return cur.fetchall()

def ingresos_hoy():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT COALESCE(SUM(dp.subtotal), 0) AS total
                FROM pedidos p
                JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
                WHERE p.fecha::date = CURRENT_DATE
                  AND p.estado = 'entregado'
            """)
            return cur.fetchone()
