from app import db
from app.models import Usuario

class UsuarioRepository:

    @staticmethod
    def add_usuario(data):
        nuevo_usuario = Usuario(
            nombre=data.get('nombre'),
            email=data.get('email'),
            telefono=data.get('telefono'),
            contrasenia=data.get('contrasenia')
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return nuevo_usuario

    @staticmethod
    def get_usuario_by_id(usuario_id):
        return Usuario.query.get(usuario_id)

    @staticmethod
    def update_usuario(usuario_id, data):
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            usuario.nombre = data.get('nombre')
            usuario.email = data.get('email')
            usuario.telefono = data.get('telefono')
            usuario.contrasenia = data.get('contrasenia')
            db.session.commit()
        return usuario

    @staticmethod
    def delete_usuario(usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
        return usuario
