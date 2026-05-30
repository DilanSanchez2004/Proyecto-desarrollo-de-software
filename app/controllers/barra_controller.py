from flask import Blueprint, render_template, request, jsonify
from app.services import mesa_service
from app.repositories.pedido_repository import obtener_pedidos_por_mesa, entregar_pedido

barra_bp = Blueprint("barra", __name__)

@barra_bp.route("/barra/pedidos")
def pedidos_barra():
    mesas = mesa_service.list_mesas()
    pedidos_agrupados = obtener_pedidos_por_mesa()
    return render_template("barra/pedidos.html", mesas=mesas, pedidos_por_mesa=pedidos_agrupados)

@barra_bp.route("/barra/pedido/<int:id_pedido>/entregar", methods=["POST"])
def entregar(id_pedido):
    ok = entregar_pedido(id_pedido)
    if ok:
        return jsonify({"ok": True})
    return jsonify({"error": "Pedido no encontrado"}), 404

@barra_bp.route("/barra/mesa/<int:id_mesa>/liberar", methods=["POST"])
def liberar_mesa(id_mesa):
    mesa_service.liberar_mesa(id_mesa)
    return jsonify({"ok": True})
