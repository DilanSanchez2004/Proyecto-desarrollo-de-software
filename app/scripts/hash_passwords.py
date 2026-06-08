import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from werkzeug.security import generate_password_hash
from app.config.db import get_connection

def es_hash_existente(contrasena):
    return contrasena.startswith(("pbkdf2:", "scrypt:", "bcrypt:", "argon2:"))

def hash_passwords():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id_usuario, contrasena FROM usuarios")
            usuarios = cur.fetchall()

        actualizados = 0
        for id_usuario, contrasena in usuarios:
            if not es_hash_existente(contrasena):
                nuevo_hash = generate_password_hash(contrasena)
                cur.execute(
                    "UPDATE usuarios SET contrasena = %s WHERE id_usuario = %s",
                    (nuevo_hash, id_usuario)
                )
                actualizados += 1
                print("  Actualizado usuario id=%s" % id_usuario)

        if actualizados > 0:
            conn.commit()
            print("\n%d contrasena(s) actualizada(s) correctamente." % actualizados)
        else:
            print("Todas las contrasenas ya estan hasheadas.")

if __name__ == "__main__":
    hash_passwords()
