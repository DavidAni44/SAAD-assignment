import os
from flask import Flask
from pymongo import MongoClient

def create_app():
    app = Flask(__name__)
    return app
