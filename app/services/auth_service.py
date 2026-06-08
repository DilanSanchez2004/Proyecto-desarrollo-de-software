from werkzeug.security import check_password_hash
from app.repositories.usuario_repository import obtener_usuario_por_correo, obtener_usuario_por_id

def autenticar_admin(correo, contrasena):
    usuario = obtener_usuario_por_correo(correo)
    if not usuario:
        return None
    if not check_password_hash(usuario["contraseña"], contrasena):
        return None
    if usuario["rol_nombre"].upper() != "ADMINISTRADOR":
        return None
    return dict(usuario)

def obtener_usuario_actual(id_usuario):
    return obtener_usuario_por_id(id_usuario)
