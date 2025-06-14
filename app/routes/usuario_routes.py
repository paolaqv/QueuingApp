from flask import Blueprint, request, jsonify
from app.services.usuario_services import UsuarioService

# Crear blueprint
usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuario')

# ----------------------------
# Ruta para crear nuevo usuario
# ----------------------------
@usuario_bp.route('/create', methods=['POST'])
def create_usuario():
    data = request.json

    campos_requeridos = ['nombre', 'email', 'telefono', 'contrasenia']
    if not all(campo in data for campo in campos_requeridos):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    nuevo_usuario = UsuarioService.create_usuario(data)
    return jsonify({
        "message": "Usuario creado exitosamente",
        "usuario": {
            "id_usuario": nuevo_usuario.id_usuario,
            "nombre": nuevo_usuario.nombre,
            "email": nuevo_usuario.email
        }
    }), 201

# ----------------------------
# Ruta de login
# ----------------------------
@usuario_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    contrasenia = data.get('contrasenia')

    if not email or not contrasenia:
        return jsonify({"error": "Faltan las credenciales"}), 400

    response, status = UsuarioService.login(email, contrasenia)
    return jsonify(response), status
