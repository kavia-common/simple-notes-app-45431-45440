from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from .routes.health import blp as health_blp
from .routes.notes import blp as notes_blp
import os

# Create Flask application and configure API docs
app = Flask(__name__)
app.url_map.strict_slashes = False

# Enable permissive CORS for simplicity (can be restricted via env if needed)
CORS(app, resources={r"/*": {"origins": "*"}})

# OpenAPI / Swagger UI configuration
app.config["API_TITLE"] = "Simple Notes API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Initialize API and register blueprints
api = Api(app)
api.register_blueprint(health_blp)
api.register_blueprint(notes_blp)

# PUBLIC_INTERFACE
def create_app():
    """Return the Flask app instance for WSGI servers."""
    return app
