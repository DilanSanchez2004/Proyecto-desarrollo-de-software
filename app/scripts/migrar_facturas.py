import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from app.config.db import get_connection

def migrar():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS facturas (
                    id_factura SERIAL PRIMARY KEY,
                    id_mesa INTEGER NOT NULL REFERENCES mesas(id_mesa),
                    numero_mesa INTEGER NOT NULL,
                    nombre_cliente VARCHAR(255),
                    fecha_emision TIMESTAMP DEFAULT NOW(),
                    total NUMERIC(12,2) NOT NULL DEFAULT 0,
                    items JSONB NOT NULL DEFAULT '[]'::jsonb,
                    created_at TIMESTAMP DEFAULT NOW()
                );
            """)
            cur.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name = 'pedidos' AND column_name = 'id_factura'
                    ) THEN
                        ALTER TABLE pedidos ADD COLUMN id_factura INTEGER REFERENCES facturas(id_factura);
                    END IF;
                END $$;
            """)
            conn.commit()
            print("Migracion completada: tabla facturas lista y columna id_factura agregada a pedidos.")

if __name__ == "__main__":
    migrar()
