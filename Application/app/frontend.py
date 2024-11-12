from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests
import json

frontend = Blueprint('frontend', __name__)

API_BASE_URL = 'http://127.0.0.1:5000/api'

@frontend.route('/')
def index():
    response = requests.get('http://127.0.0.1:5000/api/media/test')
    dict_rep = response.json() if response.status_code == 200 else {
        "message" : "fail"
    }
    
    return render_template('base.html', dict_rep=dict_rep)