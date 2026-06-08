from app.repositories.producto_repository import (
    obtener_categorias, obtener_productos,
    obtener_todos_productos, obtener_producto_por_id,
    crear_producto, actualizar_producto, eliminar_producto,
    toggle_disponible_producto
)
from app.repositories.pedido_repository import crear_pedido

def get_menu(id_categoria=None):
    categorias = obtener_categorias()
    productos  = obtener_productos(id_categoria)
    return categorias, productos

def registrar_pedido(data, id_usuario):
    return crear_pedido(
        id_mesa         = data["id_mesa"],
        id_cliente_mesa = data["id_cliente_mesa"],
        id_usuario      = id_usuario,
        tipo_pedido     = data.get("tipo_pedido", "mesa"),
        items           = data["items"]
    )

def listar_productos_admin(id_categoria=None):
    categorias = obtener_categorias()
    productos = obtener_todos_productos(id_categoria)
    return categorias, productos

def obtener_producto_admin(id_producto):
    return obtener_producto_por_id(id_producto)

def guardar_producto(nombre, descripcion, precio, id_categoria, imagen_url):
    return crear_producto(nombre, descripcion, precio, id_categoria, imagen_url)

def editar_producto(id_producto, nombre, descripcion, precio, id_categoria, disponible, imagen_url):
    return actualizar_producto(id_producto, nombre, descripcion, precio, id_categoria, disponible, imagen_url)

def quitar_producto(id_producto):
    return eliminar_producto(id_producto)

def cambiar_disponible(id_producto):
    return toggle_disponible_producto(id_producto)