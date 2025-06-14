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
    CORS(app, origins="http://localhost:5173", methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], allow_headers=["Content-Type", "Authorization"])
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.models import (Usuario, Queue, Hospital)


    from app.routes.simulation_routes import simulation_bp
    app.register_blueprint(simulation_bp)

    return app
