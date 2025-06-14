from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import datetime
from flask import current_app

class UsuarioService:

    @staticmethod
    def login(email, contrasenia): 
        usuario = UsuarioRepository.get_usuario_by_email(email)

        if not usuario:
            return {"error": "Usuario no encontrado"}, 404

        if usuario.contrasenia != contrasenia:
            return {"error": "Contraseña incorrecta"}, 401

        token = jwt.encode({
            'usuario_id': usuario.id_usuario,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        return {
            "message": "Login exitoso", 
            "id_usuario": usuario.id_usuario,
            "token": token, 
            "nombre": usuario.nombre
        }, 200

    @staticmethod
    def create_usuario(data):
        nuevo_usuario = Usuario(
            nombre=data.get('nombre'),
            email=data.get('email'),
            telefono=data.get('telefono'),
            contrasenia=data.get('contrasenia'),
            hospital_id=data.get('hospital_id')  # si es necesario
        )

        return UsuarioRepository.add_usuario(nuevo_usuario)
