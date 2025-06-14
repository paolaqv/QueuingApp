from flask import Blueprint, request, jsonify
from app.services.usuario_service import UsuarioService

# Definir el blueprint para las rutas de usuario
usuario_bp = Blueprint('usuario', __name__)

# Ruta para crear un nuevo usuario
@usuario_bp.route('/create', methods=['POST'])
def create_usuario():
    data = request.json
    nuevo_usuario = UsuarioService.create_usuario(data)
    return jsonify({"message": "Usuario creado", "usuario": nuevo_usuario.id_usuario}), 201

# Ruta para el login
@usuario_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    contrasenia = data.get('contrasenia')

    if not email or not contrasenia:
        return jsonify({"error": "Faltan las credenciales"}), 400

    response, status = UsuarioService.login(email, contrasenia)
    return jsonify(response), status
