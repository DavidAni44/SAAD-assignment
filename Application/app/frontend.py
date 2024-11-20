from flask import Blueprint, render_template, request, redirect, url_for, flash
import requests
import json

frontend = Blueprint('frontend', __name__)

API_BASE_URL = 'http://127.0.0.1:5000/api'

@frontend.route('/')
def index():
    return render_template('Index.html')



@frontend.route('/BorrowMedia')
def borrowMedia():
    response = requests.get('http://127.0.0.1:5000/api/media/test')
    dict_rep = response.json() if response.status_code == 200 else {
        "message" : "fail"
    }
    
    return render_template('BorrowMedia.html', dict_rep=dict_rep)

@frontend.route('/ManageSubscription')
def ManageSubscription():
    response = requests.get('http://127.0.0.1:5000/api/media/test')
    dict_rep = response.json() if response.status_code == 200 else {
        "message" : "fail"
    }
    
    return render_template('ManageSubscription.html', dict_rep=dict_rep)

@frontend.route('/EditUser.html')
def EditUser():
    response = requests.get('http://127.0.0.1:5000/api/media/test')
    dict_rep = response.json() if response.status_code == 200 else {
        "message" : "fail"
    }
    
    return render_template('EditUser.html', dict_rep=dict_rep)

@frontend.route('/NavBar.html')
def showNavBar():
    return render_template('NavBar.html')

@frontend.route('/AdminNavbar')
def showAdminNavBar():
    return render_template('AdminNavbar.html')

@frontend.route('/MonitorSystem.html')
def MonitorSystem():
    user_response = requests.get('http://127.0.0.1:5000/api/users/all_users')
    media_response = requests.get('http://127.0.0.1:5000/api/media/all_media').json()
    users = user_response.json() if user_response.status_code == 200 else []
    user_len = len(users)
    return render_template('MonitorSystem.html', users=users, user_len=user_len, media_response=media_response)

@frontend.route('/itemPage')
def itemPage():
    return render_template('itemPage.html')

@frontend.route('/MediaProcurement')
def mediaProcurement():
    return render_template('mediaProcurement.html')
