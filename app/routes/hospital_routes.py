import os
import json
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from app import db
from app.models.hospital import Hospital
from app.models.queue    import Queue

# Carpeta donde guardamos los JSON de simulación
THIS_DIR      = os.path.dirname(__file__)
APP_DIR       = os.path.abspath(os.path.join(THIS_DIR, '..'))
OUTPUT_FOLDER = os.path.join(APP_DIR, 'output', 'simulations')

hospital_bp = Blueprint('hospital', __name__, url_prefix='/hospitals')

@hospital_bp.route('/', methods=['GET'])
def list_hospitals():
    """
    Devuelve todos los hospitales con:
     - id
     - nombre
     - ubicacion
     - available: bool en función de avg_los < umbral (p.ej. 100 min)
    """
    umbral_los = 100  # minutos
    result = []
    for h in Hospital.query.all():
        # buscamos el último registro en queue para este hospital
        last_q = (Queue.query
                  .filter_by(hospital_id=h.id_hospital)
                  .order_by(Queue.fecha_subida.desc())
                  .first())

        available = True
        if last_q:
            # leemos su JSON
            path = os.path.join(OUTPUT_FOLDER, last_q.archivo_nombre)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                avg_los = data['metrics'].get('avg_los', 0)
                available = avg_los < umbral_los
            except Exception as e:
                current_app.logger.warning(f"No pude leer JSON {path}: {e}")
                # dejamos available=True si falla

        result.append({
            'id'         : h.id_hospital,
            'nombre'     : h.nombre,
            'ubicacion'  : h.ubicacion,
            'avg_los'   : avg_los if last_q else None,
            'available'  : available
        })

    return jsonify(result)


@hospital_bp.route('/', methods=['POST'])
def create_hospital():
    """
    Crea un nuevo hospital.
    JSON body: { nombre: str, ubicacion: str }
    """
    data = request.get_json(force=True)
    nombre    = data.get('nombre', '').strip()
    ubicacion = data.get('ubicacion', '').strip()

    if not nombre or not ubicacion:
        return jsonify(error="Los campos 'nombre' y 'ubicacion' son obligatorios"), 400

    try:
        h = Hospital(nombre=nombre, ubicacion=ubicacion)
        db.session.add(h)
        db.session.commit()
        return jsonify(h.to_dict()), 201
    except Exception as e:
        current_app.logger.exception("Error creando hospital")
        db.session.rollback()
        return jsonify(error=str(e)), 500