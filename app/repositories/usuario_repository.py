from app import db
from app.models.usuario import Usuario

class UsuarioRepository:

    @staticmethod
    def add_usuario(usuario: Usuario):
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def get_usuario_by_id(usuario_id):
        return Usuario.query.get(usuario_id)

    @staticmethod
    def get_usuario_by_email(email):
        return Usuario.query.filter_by(email=email).first()

    @staticmethod
    def update_usuario(usuario_id, data):
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            usuario.nombre = data.get('nombre', usuario.nombre)
            usuario.email = data.get('email', usuario.email)
            usuario.telefono = data.get('telefono', usuario.telefono)
            usuario.contrasenia = data.get('contrasenia', usuario.contrasenia)
            db.session.commit()
        return usuario

    @staticmethod
    def delete_usuario(usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
        return usuario
