from flask import Blueprint, request, jsonify, current_app
from app.services.simulation_service import simulate

simulation_bp = Blueprint('simulation', __name__, url_prefix='/simulate')

@simulation_bp.route('/', methods=['POST'])
def simulate_endpoint():
    try:
        params = request.get_json(force=True)
        records, metrics, plot_b64 = simulate(params)
        return jsonify({
            'metrics': metrics,
            'records': records,
            'plot_png_base64': plot_b64
        })
    except Exception as e:
        # Esto te aparecerá en la consola también
        current_app.logger.exception("Error en /simulate/")
        # Y mandamos la traza al cliente para depurar
        return jsonify({
            'error': str(e),
            'type': type(e).__name__
        }), 500
