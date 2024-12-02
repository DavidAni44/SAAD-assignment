import os
from flask import Flask
from pymongo import MongoClient
from app.routes.media import media_bp

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(media_bp)
    
    return app
