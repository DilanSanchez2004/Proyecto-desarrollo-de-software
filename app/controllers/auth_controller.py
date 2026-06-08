from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from app.services.auth_service import autenticar_admin

auth_bp = Blueprint("auth", __name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "id_usuario" not in session or session.get("rol") != "ADMINISTRADOR":
            flash("Debes iniciar sesión como administrador", "danger")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated

@auth_bp.route("/auth/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        correo = request.form.get("correo", "").strip()
        contrasena = request.form.get("contrasena", "")

        if not correo or not contrasena:
            flash("Todos los campos son obligatorios", "danger")
            return render_template("auth/login.html")

        usuario = autenticar_admin(correo, contrasena)
        if not usuario:
            flash("Credenciales inválidas o no tienes permisos de administrador", "danger")
            return render_template("auth/login.html")

        session["id_usuario"] = usuario["id_usuario"]
        session["nombre_usuario"] = usuario["nombre"]
        session["rol"] = usuario["rol_nombre"]
        flash(f"Bienvenido, {usuario['nombre']}", "success")
        return redirect(url_for("dashboard.admin_dashboard"))

    return render_template("auth/login.html")

@auth_bp.route("/auth/logout")
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for("auth.login"))
