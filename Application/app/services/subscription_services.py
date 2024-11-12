from app.services.database import user_collection, media_collection, transaction_collection, branch_collection, library_collection
from flask import request, jsonify

def manage_subscription(user_id, action):
    if action == "subscribe":
        # Add subscription to user
        user_collection.update_one({"_id": user_id}, {"$set": {"subscribed": True}})
    elif action == "unsubscribe":
        # Remove subscription from user
        user_collection.update_one({"_id": user_id}, {"$set": {"subscribed": False}})
    else:
        return jsonify({"error": "Invalid action"}), 400

    return jsonify({"message": f"User {user_id} subscription updated."}), 200