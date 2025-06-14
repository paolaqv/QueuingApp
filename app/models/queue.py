from app import db
from datetime import datetime

class Queue(db.Model):
    __tablename__ = 'queue'
    id_queue = db.Column(db.Integer, primary_key=True)
    archivo_nombre = db.Column(db.String(256))
    fecha_subida = db.Column(db.DateTime, default=datetime.utcnow)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id_hospital'))
    hospital = db.relationship('Hospital', backref='queues')