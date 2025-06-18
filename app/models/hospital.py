from app import db

class Hospital(db.Model):
    __tablename__ = 'hospital'

    id_hospital = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(128), nullable=False)
    ubicacion = db.Column(db.String(128))
    def to_dict(self):
       return {
           'id'       : self.id_hospital,
           'nombre'   : self.nombre,
           'ubicacion': self.ubicacion
       }