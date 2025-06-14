import os
import json
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from app.services.simulation_service import simulate
from app import db
from app.models.queue import Queue  # ajusta la ruta si tu modelo está en otro módulo

# Calculamos OUTPUT_FOLDER relativo a app/
THIS_DIR      = os.path.dirname(__file__)
APP_DIR       = os.path.abspath(os.path.join(THIS_DIR, '..'))
OUTPUT_FOLDER = os.path.join(APP_DIR, 'output', 'simulations')

simulation_bp = Blueprint('simulation', __name__, url_prefix='/simulate')

@simulation_bp.route('/', methods=['POST'])
def simulate_endpoint():
    try:
        # 1) Recibimos payload + el hospital_id
        payload     = request.get_json(force=True)
        hospital_id = payload.get('hospital_id')
        if hospital_id is None:
            return jsonify(error="hospital_id is required"), 400

        # 2) Ejecutamos simulación
        #    quitamos hospital_id del dict antes de pasar a simulate()
        sim_params = { **payload }
        del sim_params['hospital_id']
        records, metrics, plot_b64 = simulate(sim_params)

        # 3) Creamos carpeta si es necesario
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

        # 4) Preparamos nombre de archivo con timestamp único
        fn = f"simulation_{hospital_id}_{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}.json"
        file_path = os.path.join(OUTPUT_FOLDER, fn)

        # 5) Guardamos JSON en disco
        data = {
            'metrics': metrics,
            'records': records,
            'plot_png_base64': plot_b64
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        current_app.logger.info(f"Saved simulation output to {file_path}")

        # 6) Insertamos registro en la tabla queue
        q = Queue(
            archivo_nombre=fn,
            fecha_subida=datetime.utcnow(),
            hospital_id=hospital_id
        )
        db.session.add(q)
        db.session.commit()

        # 7) Devolvemos también el id_queue recién creado
        return jsonify({
            'metrics': metrics,
            'file_name': fn,
            'queue_id': q.id_queue
        })

    except Exception as e:
        current_app.logger.exception("Error en /simulate/")
        return jsonify(error=str(e), type=type(e).__name__), 500
