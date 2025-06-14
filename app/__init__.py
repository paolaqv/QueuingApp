from flask import Flask, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask import Flask, send_from_directory, abort

 
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Configuración de la app
    CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}}, supports_credentials=True)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.models import (Usuario, Queue, Hospital)


    from app.routes.simulation_routes import simulation_bp
    from app.routes.hospital_routes   import hospital_bp
    app.register_blueprint(simulation_bp)
    app.register_blueprint(hospital_bp)

    from app.routes import register_routes
    register_routes(app)

    @app.route('/app/output/<folder>/<filename>')
    def serve_output_file(folder, filename):
        valid_folders = ['csv', 'simulations']
        if folder not in valid_folders:
            return abort(404)

        # Ruta relativa a donde está `run.py`
        directory = os.path.abspath(os.path.join('app', 'output', folder))
        file_path = os.path.join(directory, filename)

        print("📁 Buscando en:", os.path.abspath(directory))
        print("📄 Archivo solicitado:", filename)

        if not os.path.exists(file_path):
            print("❌ Archivo NO encontrado:", os.path.abspath(file_path))
            return f"Archivo no encontrado: {file_path}", 404

        print("✅ Archivo encontrado, sirviendo:", os.path.abspath(file_path))
        return send_from_directory(directory, filename, as_attachment=True)

    return app
