import os, json
from flask import Blueprint, request, jsonify, current_app
from app.services.simulation_service import simulate

# Define salida en app/output/simulations
THIS_DIR      = os.path.dirname(__file__)
APP_DIR       = os.path.abspath(os.path.join(THIS_DIR, '..'))
OUTPUT_FOLDER = os.path.join(APP_DIR, 'output', 'simulations')

simulation_bp = Blueprint('simulation', __name__, url_prefix='/simulate')

@simulation_bp.route('/', methods=['POST'])
def simulate_endpoint():
    try:
        params        = request.get_json(force=True)
        records, metrics, plot_b64 = simulate(params)

        # Crea carpeta destino
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

        # Arma datos y guarda JSON
        data      = {'metrics': metrics, 'records': records, 'plot_png_base64': plot_b64}
        file_path = os.path.join(OUTPUT_FOLDER, 'last_simulation.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        current_app.logger.info(f"Saved simulation output to {file_path}")

        return jsonify(data)
    except Exception as e:
        current_app.logger.exception("Error en /simulate/")
        return jsonify(error=str(e), type=type(e).__name__), 500
