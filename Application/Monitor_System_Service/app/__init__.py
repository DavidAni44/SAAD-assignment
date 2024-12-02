import os
from flask import Flask
from pymongo import MongoClient
from app.routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(admin_bp)
    
    return app
