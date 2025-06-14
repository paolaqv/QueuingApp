from app import db
from app.models import Usuario
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import datetime
from flask import current_app

class UsuarioService:

    @staticmethod
    def login(email, contrasenia): 
        print(f"Email recibido: {email}")
        print(f"Contraseña recibida: {contrasenia}")
        # Busca al usuario por email
        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario:
            return {"error": "Usuario no encontrado"}, 404

        # Verifica la contraseña
        print(f"Hash en la base de datos: {usuario.contrasenia}")
        print(f"Contraseña ingresada: {contrasenia}")
        if not check_password_hash(usuario.contrasenia, contrasenia):  
            return {"error": "Contraseña incorrecta"}, 401

        # Generar el token JWT
        token = jwt.encode({
            'usuario_id': usuario.id_usuario,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        # Devuelve el token y el nombre del usuario
        return {
            "message": "Login exitoso", 
            "id_usuario": usuario.id_usuario,
            "token": token, 
            "nombre": usuario.nombre  # Devuelve el nombre del usuario
        }, 200
    @staticmethod
    def create_usuario(data):
        # Hash de la contraseña antes de almacenarla
        hashed_password = generate_password_hash(data.get('contrasenia'))

        nuevo_usuario = Usuario(
            nombre=data.get('nombre'),
            email=data.get('email'),
            telefono=data.get('telefono'),
            contrasenia=hashed_password
        )
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return nuevo_usuario