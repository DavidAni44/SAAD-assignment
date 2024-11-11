from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Load environment variables
DBUSERNAME = os.getenv("DBUSERNAME")
DBPASSWORD = os.getenv("DBPASSWORD")
MEDIA_SERVICE_URL = os.getenv("MEDIA_SERVICE_URL")

# Define routes to forward requests to the appropriate microservices

# Borrow Media
@app.route('/borrow_media', methods=['POST'])
def borrow_media():
    media_id = request.json.get('media_id')
    user_id = request.json.get('user_id')
    
    # Forward to Borrow Service
    response = requests.post(f"{MEDIA_SERVICE_URL}/borrow_media", json={"media_id": media_id, "user_id": user_id})
    return jsonify(response.json()), response.status_code

# Reserve Media
@app.route('/reserve_media', methods=['POST'])
def reserve_media():
    media_id = request.json.get('media_id')
    user_id = request.json.get('user_id')
    
    # Forward to Reserve Service
    response = requests.post(f"{MEDIA_SERVICE_URL}/reserve_media", json={"media_id": media_id, "user_id": user_id})
    return jsonify(response.json()), response.status_code

# Manage Subscriptions
@app.route('/manage_subscription', methods=['POST'])
def manage_subscription():
    user_id = request.json.get('user_id')
    action = request.json.get('action')  # subscribe, unsubscribe, etc.
    
    # Forward to Subscription Service
    response = requests.post(f"{MEDIA_SERVICE_URL}/manage_subscription", json={"user_id": user_id, "action": action})
    return jsonify(response.json()), response.status_code

# Media Procurement
@app.route('/procure_media', methods=['POST'])
def procure_media():
    media_details = request.json
    
    # Forward to Procurement Service
    response = requests.post(f"{MEDIA_SERVICE_URL}/procure_media", json=media_details)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
