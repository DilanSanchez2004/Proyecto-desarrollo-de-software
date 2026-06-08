from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app.repositories.usuario_repository import (
    obtener_usuarios_admin, obtener_usuario_por_correo,
    crear_usuario, eliminar_usuario, obtener_rol_admin
)
from app.controllers.auth_controller import admin_required

usuario_bp = Blueprint("usuario", __name__)

@usuario_bp.route("/admin/usuarios")
@admin_required
def admin_usuarios():
    usuarios = obtener_usuarios_admin()
    return render_template("admin/usuarios.html", usuarios=usuarios)

@usuario_bp.route("/admin/usuarios/crear", methods=["POST"])
@admin_required
def admin_crear_usuario():
    nombre = request.form.get("nombre", "").strip()
    correo = request.form.get("correo", "").strip()
    contrasena = request.form.get("contrasena", "")

    if not nombre or not correo or not contrasena:
        flash("Todos los campos son obligatorios", "danger")
        return redirect(url_for("usuario.admin_usuarios"))

    if obtener_usuario_por_correo(correo):
        flash("Ya existe un usuario con ese correo", "danger")
        return redirect(url_for("usuario.admin_usuarios"))

    if len(contrasena) < 6:
        flash("La contraseña debe tener al menos 6 caracteres", "danger")
        return redirect(url_for("usuario.admin_usuarios"))

    try:
        hash_contrasena = generate_password_hash(contrasena)
        id_rol = obtener_rol_admin()
        crear_usuario(nombre, correo, hash_contrasena, id_rol)
        flash(f"Administrador '{nombre}' creado exitosamente", "success")
    except Exception as e:
        flash(f"Error al crear usuario: {str(e)}", "danger")

    return redirect(url_for("usuario.admin_usuarios"))

@usuario_bp.route("/admin/usuarios/<int:id_usuario>/eliminar", methods=["POST"])
@admin_required
def admin_eliminar_usuario(id_usuario):
    from flask import session
    if id_usuario == session.get("id_usuario"):
        flash("No puedes eliminarte a ti mismo", "danger")
        return redirect(url_for("usuario.admin_usuarios"))

    try:
        eliminar_usuario(id_usuario)
        flash("Usuario eliminado exitosamente", "success")
    except Exception as e:
        flash(f"Error al eliminar usuario: {str(e)}", "danger")

    return redirect(url_for("usuario.admin_usuarios"))
