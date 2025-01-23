from flask import Flask, current_app, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from app.logging_config import configure_logging
from logging.config import dictConfig

from app.exceptions import AppException

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(filename)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Configure logging
    # configure_logging(app)

    # Import and register blueprints
    from app.routes.projects import projects_bp
    from app.routes.query import query_bp
    # from app.routes.chats import chats_bp

    app.register_blueprint(projects_bp, url_prefix="/api/projects/")
    app.register_blueprint(query_bp, url_prefix="/api/query/")
    # app.register_blueprint(chats_bp, url_prefix="/api/chats")

    
    register_error_handlers(app)
    return app


def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        status_code = 500
        message = str(e)

        if isinstance(e, AppException):
            status_code = e.status_code
            message = e.message
            payload = e.payload
            current_app.logger.error(f"Error: {payload}")
        else:
            current_app.logger.error(f"Error: {message}")
        return jsonify({"error": message}), status_code