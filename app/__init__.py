from flask import Flask, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

 
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
    app.register_blueprint(simulation_bp)

    from app.routes import register_routes
    register_routes(app)
    return app
