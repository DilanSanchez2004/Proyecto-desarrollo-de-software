from app.config.db import get_connection
from psycopg2.extras import RealDictCursor

def obtener_usuario_por_correo(correo):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT u.id_usuario, u.nombre, u.correo, u.contrasena, u.id_rol,
                       r.nombre AS rol_nombre
                FROM usuarios u
                JOIN roles r ON u.id_rol = r.id_rol
                WHERE u.correo = %s
            """, (correo,))
            return cur.fetchone()

def obtener_usuario_por_id(id_usuario):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT u.id_usuario, u.nombre, u.correo, u.id_rol, r.nombre AS rol_nombre
                FROM usuarios u
                JOIN roles r ON u.id_rol = r.id_rol
                WHERE u.id_usuario = %s
            """, (id_usuario,))
            return cur.fetchone()

def obtener_usuarios_admin():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT u.id_usuario, u.nombre, u.correo, u.id_rol, r.nombre AS rol_nombre
                FROM usuarios u
                JOIN roles r ON u.id_rol = r.id_rol
                WHERE r.nombre = 'admin'
                ORDER BY u.nombre
            """)
            return cur.fetchall()

def obtener_rol_admin():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id_rol FROM roles WHERE nombre = 'admin'")
            row = cur.fetchone()
            if row:
                return row[0]
            cur.execute("INSERT INTO roles (nombre) VALUES ('admin') RETURNING id_rol")
            id_rol = cur.fetchone()[0]
            conn.commit()
            return id_rol

def crear_usuario(nombre, correo, contrasena_hash, id_rol):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO usuarios (nombre, correo, contrasena, id_rol)
                VALUES (%s, %s, %s, %s)
                RETURNING id_usuario
            """, (nombre, correo, contrasena_hash, id_rol))
            id_usuario = cur.fetchone()[0]
        conn.commit()
    return id_usuario

def eliminar_usuario(id_usuario):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            deleted = cur.rowcount
        conn.commit()
    return deleted
