from flask import Flask
from flask_cors import CORS  # Import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for the whole app

    # Register blueprints or routes
    from app.routes import api_bp
    app.register_blueprint(api_bp)

    return app
