import os
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from .api import init_api
from app.frontend import frontend

# Load environment variables from .env file
load_dotenv()

# Initialize the MongoDB client outside of the create_app function for global use


def create_app():
    # Correct the path for static_folder
    app = Flask(__name__, template_folder='templates', static_folder='static')
    CORS(app, resources={r"/*": {
        "origins": "*",  # You can restrict this to specific origins if needed
        "methods": ["GET", "POST", "DELETE", "OPTIONS"],  # Allowed methods
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"]  # Allowed headers
    }})
    init_api(app)
    app.register_blueprint(frontend)

    return app
