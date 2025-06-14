from app import db

class Usuario(db.Model):
    __tablename__ = 'Usuario'
    
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(70), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    contrasenia = db.Column(db.String(255), nullable=False)

