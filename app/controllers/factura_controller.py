from flask import Blueprint, render_template, jsonify, session, redirect, url_for
from app.repositories.factura_repository import obtener_facturas, obtener_factura_por_id
from app.controllers.auth_controller import admin_required

factura_bp = Blueprint("factura", __name__)

@factura_bp.route("/admin/facturas")
@admin_required
def admin_facturas():
    facturas = obtener_facturas()
    return render_template("admin/facturas.html", facturas=facturas)

@factura_bp.route("/factura/<int:id_factura>/imprimir")
def imprimir_factura(id_factura):
    factura = obtener_factura_por_id(id_factura)
    if not factura:
        return "Factura no encontrada", 404
    return render_template("factura/print.html", factura=factura)

@factura_bp.route("/factura/<int:id_factura>/json")
def factura_json(id_factura):
    factura = obtener_factura_por_id(id_factura)
    if not factura:
        return jsonify({"error": "Factura no encontrada"}), 404
    factura["items"] = factura.get("items") or []
    return jsonify(dict(factura))
