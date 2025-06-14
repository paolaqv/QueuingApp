from app.repositories.queue_repository import QueueRepository

class QueueService:
    @staticmethod
    def get_files_by_hospital(hospital_id):
        return QueueRepository.get_file_names_by_hospital(hospital_id)
