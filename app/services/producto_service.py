from app.repositories.producto_repository import obtener_categorias, obtener_productos
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