from flask import Blueprint, render_template
from app.services.dashboard_service import obtener_resumen
from app.controllers.auth_controller import admin_required

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    resumen = obtener_resumen()
    return render_template("admin/dashboard.html", resumen=resumen)
