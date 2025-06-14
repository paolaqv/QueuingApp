from app.models.queue import Queue

class QueueRepository:
    @staticmethod
    def get_file_names_by_hospital(hospital_id):
        queues = Queue.query.filter_by(hospital_id=hospital_id).all()
        return [q.archivo_nombre for q in queues]
