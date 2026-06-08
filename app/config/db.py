import os
import psycopg2

os.environ.setdefault("PGCLIENTENCODING", "UTF8")

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="proyyyyyyyy",
        user="postgres",
        password="Santi.26"
    )
    conn.set_client_encoding("UTF8")
    return conn
