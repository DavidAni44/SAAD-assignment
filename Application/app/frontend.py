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
    response = requests.get('http://127.0.0.1:5000/api/media/all_branch_media')
    dict_rep = response.json() if response.status_code == 200 else []

    #hardcoded for Mountain Branch. change to be whatever branch user is on. may need to move this logic into the html page
    mountain_branch_data = None
    for branch in dict_rep:  
        if (branch.get('branch')).get('name') == "Mountain Branch": 
            print("yahoo")
            mountain_branch_data = branch
            break

    if mountain_branch_data is None:
        print("Mountain Branch not found.")
        return render_template('BorrowMedia.html', media=[], page=1, total_pages=1)

    media_list = mountain_branch_data.get('media', [])

    page = int(request.args.get('page', 1))
    items_per_page = 6
    start = (page - 1) * items_per_page
    end = start + items_per_page
    paginated_media = media_list[start:end]
    total_pages = (len(media_list) + items_per_page - 1) // items_per_page

    return render_template('BorrowMedia.html', media=paginated_media, page=page, total_pages=total_pages)

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
    response = requests.get('http://127.0.0.1:5000/api/media/all_branch_media')
    dict_rep = response.json() if response.status_code == 200 else []

    all_media = []
    for branch in dict_rep:  
        all_media.extend(branch.get('media', []))

    if not all_media:
        print("No media found.")
        return render_template('ProcureMediaChoices.html', media=[], page=1, total_pages=1)


    page = int(request.args.get('page', 1))
    items_per_page = 9
    start = (page - 1) * items_per_page
    end = start + items_per_page
    paginated_media = all_media[start:end]
    total_pages = (len(all_media) + items_per_page - 1) // items_per_page
    print(total_pages)

    return render_template('ProcureMediaChoices.html', media=paginated_media, page=page, total_pages=total_pages)

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


