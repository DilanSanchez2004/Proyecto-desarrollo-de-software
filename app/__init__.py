from flask import Flask
from app.controllers.producto_controller import producto_bp
from app.controllers.mesa_controller import mesa_bp
from app.controllers.barra_controller import barra_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'cambia_esta_clave_secreta'

    # Registrar blueprints
    app.register_blueprint(producto_bp)
    app.register_blueprint(mesa_bp)
    app.register_blueprint(barra_bp)

    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('producto.menu'))

    return app
