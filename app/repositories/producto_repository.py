from app.config.db import get_connection
from psycopg2.extras import RealDictCursor

def obtener_categorias():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id_categoria, nombre FROM categorias ORDER BY nombre")
            return cur.fetchall()

def obtener_productos(id_categoria=None):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if id_categoria:
                cur.execute("""
                    SELECT p.id_producto, p.nombre, p.descripcion,
                           p.precio, p.imagen_url, c.nombre AS categoria
                    FROM productos p
                    JOIN categorias c ON p.id_categoria = c.id_categoria
                    WHERE p.disponible = TRUE
                      AND p.id_categoria = %s
                    ORDER BY p.nombre
                """, (id_categoria,))
            else:
                cur.execute("""
                    SELECT p.id_producto, p.nombre, p.descripcion,
                           p.precio, p.imagen_url, c.nombre AS categoria
                    FROM productos p
                    JOIN categorias c ON p.id_categoria = c.id_categoria
                    WHERE p.disponible = TRUE
                    ORDER BY c.nombre, p.nombre
                """)
            return cur.fetchall()