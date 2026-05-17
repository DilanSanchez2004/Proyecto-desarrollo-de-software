from flask import Blueprint, render_template, request, jsonify, session
from app.services.producto_service import get_menu, registrar_pedido

menu_bp = Blueprint("menu", __name__)


@menu_bp.route("/menu")
def menu():
    """
    Muestra el menú completo.
    Acepta ?categoria=<id> para filtrar por categoría.
    """
    id_categoria = request.args.get("categoria", type=int)

    categorias, productos = get_menu(id_categoria)

    return render_template(
        "cliente/menu.html",
        categorias=categorias,
        productos=productos,
        categoria_activa=id_categoria
    )


@menu_bp.route("/pedido", methods=["POST"])
def crear_pedido_endpoint():
    """
    Recibe el carrito desde el frontend y lo guarda en la BD.

    Body JSON esperado:
    {
        "id_mesa": 1,
        "id_cliente_mesa": 2,
        "tipo_pedido": "mesa",
        "items": [
            {
                "id_producto": 5,
                "cantidad": 2,
                "precio_unitario": 19500
            }
        ]
    }
    """
    data = request.get_json()

    campos = ["id_mesa", "id_cliente_mesa", "items"]
    for campo in campos:
        if campo not in data:
            return jsonify({"error": f"Falta el campo: {campo}"}), 400

    if not data["items"]:
        return jsonify({"error": "El carrito está vacío"}), 400

    id_usuario = session.get("id_usuario")

    try:
        id_pedido = registrar_pedido(data, id_usuario)
        return jsonify({"ok": True, "id_pedido": id_pedido}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500