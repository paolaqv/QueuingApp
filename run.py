from flask import Flask, send_from_directory, abort
import os

# Crear app directamente aquí (no con factory)
app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)
