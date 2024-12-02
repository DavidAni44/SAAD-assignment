from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.database import user_collection, subscription_collection
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
def procureMediaChoices():
    return render_template('ProcureMediaChoices.html')

@frontend.route('/mediaSuccessfullyOrdered')
def mediaSuccessfullyOrdered():
    return render_template('mediaSuccessfullyOrdered.html')

@frontend.route('/ManageSubscription')
def manage_subscription():
    # Get pagination parameters from query arguments
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)
    skip = (page - 1) * limit

    # Fetch paginated users
    users = list(user_collection.find().skip(skip).limit(limit))
    subscriptions = list(subscription_collection.find())

    # Ensure IDs are strings for consistent comparison in the template
    for user in users:
        user["subscription_id"] = str(user.get("subscription_id", ""))
    for subscription in subscriptions:
        subscription["subscription_id"] = str(subscription.get("subscription_id", ""))

    return render_template(
        "ManageSubscription.html",
        users=users,
        subscriptions=subscriptions,
        current_page=page,
        limit=limit
    )