from flask import Blueprint, render_template, request, jsonify, session
from app.services.producto_service import get_menu, registrar_pedido

producto_bp = Blueprint("producto", __name__)


@producto_bp.route("/menu")
def menu():
    id_categoria = request.args.get("categoria", type=int)
    categorias, productos = get_menu(id_categoria)
    return render_template(
        "cliente/menu.html",
        categorias=categorias,
        productos=productos,
        categoria_activa=id_categoria
    )


@producto_bp.route("/pedido", methods=["POST"])
def pedido():
    data = request.get_json()

    for campo in ["id_mesa", "id_cliente_mesa", "items"]:
        if campo not in data:
            return jsonify({"error": f"Falta el campo: {campo}"}), 400

    if not data["items"]:
        return jsonify({"error": "El carrito esta vacio"}), 400

    try:
        id_usuario = session.get("id_usuario")
        id_pedido = registrar_pedido(data, id_usuario)
        return jsonify({"ok": True, "id_pedido": id_pedido}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
