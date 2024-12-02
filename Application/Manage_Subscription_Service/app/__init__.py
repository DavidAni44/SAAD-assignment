import os
from flask import Flask
from pymongo import MongoClient
from app.routes.subscriptions import subscription_bp

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(subscription_bp)
    
    return app
