from app import db

class Hospital(db.Model):
    __tablename__ = 'Hospital'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False)
    ubicacion = db.Column(db.String(128))