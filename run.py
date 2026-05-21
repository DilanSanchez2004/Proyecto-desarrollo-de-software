import os
import sys

sys.path.insert(0, os.path.abspath("."))

from app import create_app

app = create_app()

if __name__ == "__main__":
    print("Iniciando servidor Flask...")
    print("Accede a: http://127.0.0.1:5000/menu")
    app.run(debug=True, port=5000, host="127.0.0.1")
