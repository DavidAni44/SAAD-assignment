from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient(f'mongodb+srv://{os.getenv("DBUSERNAME")}:{os.getenv("DBPASSWORD")}@your-cluster-url')
db = client["AMLdb"]
user_collection = db["User Data"]

@app.route('/manage_subscription', methods=['POST'])
def manage_subscription():
    user_id = request.json.get('user_id')
    action = request.json.get('action')  # subscribe, unsubscribe, etc.
    
    if action == "subscribe":
        # Add subscription to user
        user_collection.update_one({"_id": user_id}, {"$set": {"subscribed": True}})
    elif action == "unsubscribe":
        # Remove subscription from user
        user_collection.update_one({"_id": user_id}, {"$set": {"subscribed": False}})
    else:
        return jsonify({"error": "Invalid action"}), 400
    
    return jsonify({"message": f"User {user_id} subscription updated."}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
