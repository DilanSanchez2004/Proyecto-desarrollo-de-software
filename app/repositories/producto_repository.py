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

def obtener_todos_productos(id_categoria=None):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if id_categoria:
                cur.execute("""
                    SELECT p.id_producto, p.nombre, p.descripcion, p.precio,
                           p.disponible, p.imagen_url, p.id_categoria, c.nombre AS categoria
                    FROM productos p
                    JOIN categorias c ON p.id_categoria = c.id_categoria
                    WHERE p.id_categoria = %s
                    ORDER BY p.nombre
                """, (id_categoria,))
            else:
                cur.execute("""
                    SELECT p.id_producto, p.nombre, p.descripcion, p.precio,
                           p.disponible, p.imagen_url, p.id_categoria, c.nombre AS categoria
                    FROM productos p
                    JOIN categorias c ON p.id_categoria = c.id_categoria
                    ORDER BY c.nombre, p.nombre
                """)
            return cur.fetchall()

def obtener_producto_por_id(id_producto):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT p.id_producto, p.nombre, p.descripcion, p.precio,
                       p.disponible, p.imagen_url, p.id_categoria
                FROM productos p
                WHERE p.id_producto = %s
            """, (id_producto,))
            return cur.fetchone()

def crear_producto(nombre, descripcion, precio, id_categoria, imagen_url):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO productos (nombre, descripcion, precio, id_categoria, imagen_url, disponible)
                VALUES (%s, %s, %s, %s, %s, TRUE)
                RETURNING id_producto
            """, (nombre, descripcion, precio, id_categoria, imagen_url))
            id_producto = cur.fetchone()[0]
        conn.commit()
    return id_producto

def actualizar_producto(id_producto, nombre, descripcion, precio, id_categoria, disponible, imagen_url):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE productos SET nombre = %s, descripcion = %s, precio = %s,
                    id_categoria = %s, disponible = %s, imagen_url = %s
                WHERE id_producto = %s
            """, (nombre, descripcion, precio, id_categoria, disponible, imagen_url, id_producto))
            updated = cur.rowcount
        conn.commit()
    return updated

def eliminar_producto(id_producto):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
            deleted = cur.rowcount
        conn.commit()
    return deleted

def toggle_disponible_producto(id_producto):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE productos SET disponible = NOT disponible WHERE id_producto = %s
                RETURNING disponible
            """, (id_producto,))
            nuevo_estado = cur.fetchone()[0]
        conn.commit()
    return nuevo_estado