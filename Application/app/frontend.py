from flask import Blueprint, render_template, request, redirect, url_for, flash
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import requests
import json

frontend = Blueprint('frontend', __name__)

API_BASE_URL = 'http://127.0.0.1:5000/api'

def ping_endpoint():
    try:
        response = requests.get('http://127.0.0.1:5000/api/users/ping')  # Replace with your actual endpoint
        print(f"Pinged API. Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error pinging API: {e}")
        

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

@frontend.route('/MonitorSystem')
def MonitorSystem():
    user_response = requests.get('http://127.0.0.1:5000/api/users/all_users')
    media_response = requests.get('http://127.0.0.1:5000/api/media/all_media').json()
    branch_response = requests.get('http://127.0.0.1:5000/api/media/all_branches').json()
    all_branch_media = requests.get('http://127.0.0.1:5000/api/media/all_branch_media').json()
    users = user_response.json() if user_response.status_code == 200 else []
    user_len = len(users)
    return render_template('MonitorSystem.html', users=users, user_len=user_len, media_response=media_response, branches=branch_response, all_branch_media=all_branch_media)

@frontend.route('/itemPage')
def itemPage():
    return render_template('itemPage.html')

@frontend.route('/MediaProcurement')
def mediaProcurement():
    return render_template('mediaProcurement.html')

@frontend.route('/GenerateReport')
def GenerateReport():
    return render_template('GenerateReport.html')

@frontend.route('/SuccessBorrow')
def successBorrow():
    return render_template('successBorrow.html')

@frontend.route('/ProcureMediaChoices')
def ProcureMediaChoices():
    return render_template('ProcureMediaChoices.html')

@frontend.route('/mediaSuccessfullyOrdered')
def mediaSuccessfullyOrdered():
    return render_template('mediaSuccessfullyOrdered.html')