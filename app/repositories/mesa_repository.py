from app.config.db import get_connection
from psycopg2.extras import RealDictCursor

def obtener_mesas():
    """
    Obtiene todas las mesas ordenadas por su número.
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id_mesa, numero_mesa, estado FROM mesas ORDER BY numero_mesa")
            return cur.fetchall()

def crear_mesa(numero_mesa, estado="libre"):
    """
    Crea una nueva mesa en la base de datos.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO mesas (numero_mesa, estado)
                VALUES (%s, %s)
                RETURNING id_mesa
            """, (numero_mesa, estado))
            id_mesa = cur.fetchone()[0]
        conn.commit()
    return id_mesa

def obtener_mesa_por_id(id_mesa):
    """
    Obtiene los detalles de una mesa por su ID.
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id_mesa, numero_mesa, estado FROM mesas WHERE id_mesa = %s", (id_mesa,))
            return cur.fetchone()

def ocupar_mesa(id_mesa):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE mesas SET estado = 'ocupada' WHERE id_mesa = %s",
                (id_mesa,)
            )
        conn.commit()

def liberar_mesa(id_mesa):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE mesas SET estado = 'libre' WHERE id_mesa = %s",
                (id_mesa,)
            )
        conn.commit()

def registrar_cliente_mesa(nombre, id_mesa):
    """
    Registra un cliente asociado a una mesa y retorna el id_cliente_mesa generado.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO clientes_mesa (nombre, id_mesa)
                VALUES (%s, %s)
                RETURNING id_cliente_mesa
            """, (nombre, id_mesa))
            id_cliente_mesa = cur.fetchone()[0]
        conn.commit()
    return id_cliente_mesa


def eliminar_mesa(id_mesa):
    """
    Elimina una mesa por su ID, incluyendo sus referencias.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM detalle_pedido WHERE id_pedido IN (SELECT id_pedido FROM pedidos WHERE id_mesa = %s)", (id_mesa,))
            cur.execute("DELETE FROM pedidos WHERE id_mesa = %s", (id_mesa,))
            cur.execute("DELETE FROM clientes_mesa WHERE id_mesa = %s", (id_mesa,))
            cur.execute("DELETE FROM mesas WHERE id_mesa = %s", (id_mesa,))
            deleted = cur.rowcount
        conn.commit()
    return deleted
