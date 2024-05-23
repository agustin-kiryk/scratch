import sys
import os

# Añade el directorio 'src' al sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from App_factory import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)