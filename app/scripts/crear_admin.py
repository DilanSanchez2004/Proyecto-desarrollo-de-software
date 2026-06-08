import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from werkzeug.security import generate_password_hash
from app.config.db import get_connection

def crear_admin(nombre=None, correo=None, contrasena=None):
    if not nombre:
        nombre = input("Nombre: ").strip()
    if not correo:
        correo = input("Correo electronico: ").strip()
    if not contrasena:
        contrasena = input("Contrasena: ").strip()

    if not nombre or not correo or not contrasena:
        print("Todos los campos son obligatorios.")
        return

    hash_contrasena = generate_password_hash(contrasena)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id_rol FROM roles WHERE UPPER(nombre) = 'ADMINISTRADOR'")
            row = cur.fetchone()
            if not row:
                print("No existe el rol 'ADMINISTRADOR' en la tabla roles. Creandolo...")
                cur.execute(
                    "INSERT INTO roles (nombre) VALUES ('ADMINISTRADOR') RETURNING id_rol"
                )
                id_rol = cur.fetchone()[0]
                conn.commit()
            else:
                id_rol = row[0]

            cur.execute(
                """
                INSERT INTO usuarios (nombre, correo, contraseña, id_rol)
                VALUES (%s, %s, %s, %s)
                """,
                (nombre, correo, hash_contrasena, id_rol)
            )
            conn.commit()

    print(f"Administrador '{nombre}' creado exitosamente con correo '{correo}'.")

if __name__ == "__main__":
    import sys
    args = [a.strip() for a in sys.argv[1:3]]
    kwargs = {}
    if len(sys.argv) > 3:
        kwargs = {"nombre": sys.argv[1], "correo": sys.argv[2], "contrasena": sys.argv[3]}
    crear_admin(**kwargs)
