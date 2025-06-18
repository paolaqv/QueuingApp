from app import db

class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(70), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    contrasenia = db.Column(db.String(255), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id_hospital'))
    hospital = db.relationship('Hospital', backref='usuario')

    def to_dict(self):
        return {
            'id'        : self.id_usuario,
            'nombre'    : self.nombre,
            'email'     : self.email,
            'hospital_id': self.hospital_id
        }
