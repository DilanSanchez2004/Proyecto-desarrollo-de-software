from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from app.services.producto_service import get_menu, registrar_pedido, listar_productos_admin, obtener_producto_admin, guardar_producto, editar_producto, quitar_producto, cambiar_disponible
from app.services import mesa_service
from app.controllers.auth_controller import admin_required

producto_bp = Blueprint("producto", __name__)


@producto_bp.route("/menu")
def menu():
    id_categoria = request.args.get("categoria", type=int)
    categorias, productos = get_menu(id_categoria)
    mesa = mesa_service.get_mesa_by_id(session.get("id_mesa")) if session.get("id_mesa") else None
    return render_template(
        "cliente/menu.html",
        categorias=categorias,
        productos=productos,
        categoria_activa=id_categoria,
        mesa=mesa
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

@producto_bp.route("/admin/productos")
@admin_required
def admin_productos():
    id_categoria = request.args.get("categoria", type=int)
    categorias, productos = listar_productos_admin(id_categoria)
    return render_template("admin/productos.html", categorias=categorias, productos=productos, categoria_activa=id_categoria)

@producto_bp.route("/admin/productos/crear", methods=["POST"])
@admin_required
def admin_crear_producto():
    nombre = request.form.get("nombre", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    precio = request.form.get("precio", type=float)
    id_categoria = request.form.get("id_categoria", type=int)
    imagen_url = request.form.get("imagen_url", "").strip()

    if not nombre or not precio or not id_categoria:
        flash("Nombre, precio y categoría son obligatorios", "danger")
        return redirect(url_for("producto.admin_productos"))

    try:
        guardar_producto(nombre, descripcion, precio, id_categoria, imagen_url or None)
        flash("Producto creado exitosamente", "success")
    except Exception as e:
        flash(f"Error al crear producto: {str(e)}", "danger")

    return redirect(url_for("producto.admin_productos"))

@producto_bp.route("/admin/productos/<int:id_producto>/editar", methods=["POST"])
@admin_required
def admin_editar_producto(id_producto):
    nombre = request.form.get("nombre", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    precio = request.form.get("precio", type=float)
    id_categoria = request.form.get("id_categoria", type=int)
    disponible = request.form.get("disponible") == "true"
    imagen_url = request.form.get("imagen_url", "").strip()

    if not nombre or not precio or not id_categoria:
        flash("Nombre, precio y categoría son obligatorios", "danger")
        return redirect(url_for("producto.admin_productos"))

    try:
        editar_producto(id_producto, nombre, descripcion, precio, id_categoria, disponible, imagen_url or None)
        flash("Producto actualizado exitosamente", "success")
    except Exception as e:
        flash(f"Error al actualizar producto: {str(e)}", "danger")

    return redirect(url_for("producto.admin_productos"))

@producto_bp.route("/admin/productos/<int:id_producto>/eliminar", methods=["POST"])
@admin_required
def admin_eliminar_producto(id_producto):
    try:
        quitar_producto(id_producto)
        flash("Producto eliminado exitosamente", "success")
    except Exception as e:
        flash(f"Error al eliminar producto: {str(e)}", "danger")
    return redirect(url_for("producto.admin_productos"))

@producto_bp.route("/admin/productos/<int:id_producto>/toggle", methods=["POST"])
@admin_required
def admin_toggle_producto(id_producto):
    try:
        nuevo_estado = cambiar_disponible(id_producto)
        return jsonify({"ok": True, "disponible": nuevo_estado})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
