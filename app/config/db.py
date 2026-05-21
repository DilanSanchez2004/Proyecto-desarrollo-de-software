import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="bocado",
        user="postgres",
        password="18abril3"
    )
    conn.set_client_encoding("UTF8")
    return conn
