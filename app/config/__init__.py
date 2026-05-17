import os
from flask import Flask

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, 'templates'),
        static_folder=os.path.join(base_dir, 'static')
    )
    app.secret_key = 'clave_secreta_bocado_rapido'

    from app.controllers.producto_controller import producto_bp
    app.register_blueprint(producto_bp)

    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('producto.menu'))

    return app
