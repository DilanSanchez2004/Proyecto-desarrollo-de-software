from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.services import mesa_service
from app.controllers.auth_controller import admin_required

mesa_bp = Blueprint("mesa", __name__)

@mesa_bp.route("/admin/mesas")
@admin_required
def admin_mesas():
    """
    Panel de administración para listar mesas y generar códigos QR.
    """
    mesas = mesa_service.list_mesas()
    return render_template("admin/mesas.html", mesas=mesas)

@mesa_bp.route("/admin/mesas/crear", methods=["POST"])
@admin_required
def crear_mesa():
    """
    Registrar una nueva mesa en el sistema.
    """
    numero_mesa = request.form.get("numero_mesa", type=int)
    if numero_mesa is not None:
        try:
            mesa_service.register_mesa(numero_mesa)
            flash("Mesa creada exitosamente", "success")
        except Exception as e:
            flash(f"Error al crear la mesa: {str(e)}", "danger")
    else:
        flash("El número de mesa es requerido", "warning")
    return redirect(url_for("mesa.admin_mesas"))

@mesa_bp.route("/mesa/<int:id_mesa>")
def welcome_mesa(id_mesa):
    """
    Página de bienvenida que el cliente ve tras escanear el código QR de la mesa.
    """
    mesa = mesa_service.get_mesa_by_id(id_mesa)
    if not mesa:
        return "La mesa solicitada no existe.", 404
    
    return render_template("cliente/registro_mesa.html", mesa=mesa)

@mesa_bp.route("/mesa/<int:id_mesa>/registro", methods=["POST"])
def registrar_cliente(id_mesa):
    """
    Registra el nombre del cliente y asigna la mesa en la sesión actual.
    """
    nombre_cliente = request.form.get("nombre")
    if not nombre_cliente or not nombre_cliente.strip():
        flash("El nombre es obligatorio para realizar pedidos.", "warning")
        return redirect(url_for("mesa.welcome_mesa", id_mesa=id_mesa))
    
    try:
        # Registrar en tabla clientes_mesa y ocupar la mesa
        id_cliente_mesa = mesa_service.register_client_for_table(nombre_cliente.strip(), id_mesa)
        mesa_service.ocupar_mesa(id_mesa)
        
        # Almacenar datos en sesión de Flask
        session["id_mesa"] = id_mesa
        session["id_cliente_mesa"] = id_cliente_mesa
        session["tipo_pedido"] = "mesa"
        
        return redirect(url_for("producto.menu"))
    except Exception as e:
        flash(f"Error al registrarse: {str(e)}", "danger")
        return redirect(url_for("mesa.welcome_mesa", id_mesa=id_mesa))


@mesa_bp.route("/admin/mesas/<int:id_mesa>/eliminar", methods=["POST"])
@admin_required
def eliminar_mesa(id_mesa):
    """
    Elimina una mesa del sistema.
    """
    try:
        mesa_service.delete_mesa(id_mesa)
        flash("Mesa eliminada exitosamente", "success")
    except Exception as e:
        flash(f"Error al eliminar la mesa: {str(e)}", "danger")
    return redirect(url_for("mesa.admin_mesas"))
