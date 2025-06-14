from flask import Blueprint, jsonify
from app.services.queue_service import QueueService

queue_bp = Blueprint('queue_bp', __name__, url_prefix='/queue')


@queue_bp.route('/files/<int:hospital_id>', methods=['GET'])
def get_files_by_hospital(hospital_id):
    try:
        archivos = QueueService.get_files_by_hospital(hospital_id)
        return jsonify({"files": archivos}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
