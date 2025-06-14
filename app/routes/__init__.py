from flask import Blueprint
from .usuario_routes import usuario_bp
from .queue_routes import queue_bp

# blueprints
def register_routes(app):
    app.register_blueprint(usuario_bp, url_prefix='/usuario')
    app.register_blueprint(queue_bp, url_prefix='/queue')
