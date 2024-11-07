from flask import Flask, render_template, request, jsonify
from flask import Flask, render_template, redirect, request, session
from pymongo import MongoClient
from bson.json_util import dumps
import json
import os
from dotenv import load_dotenv, dotenv_values


app = Flask(__name__, template_folder='templates', static_folder='/static')

client = MongoClient(f'mongodb+srv://{os.getenv("DBUSERNAME")}:{os.getenv("DBPASSWORD")}@saaddatabase.8f32e.mongodb.net/?retryWrites=true&w=majority&appName=SAADdatabase')
db= client["AMLdb"]
collection = db["AMLDB"]

@app.route('/')
def index():
    documents = list(collection.find())
    obj_json = dumps(documents, indent=2)
    return obj_json
    
    
        


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)