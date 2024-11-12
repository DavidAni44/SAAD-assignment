import os
from flask import Flask
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
    init_api(app)
    app.register_blueprint(frontend)

    return app
