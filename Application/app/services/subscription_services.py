from app.services.database import user_collection, media_collection, transaction_collection, branch_collection, library_collection
from flask import request, jsonify

def edit_subscription(user_id, new_subscription):
    try:
        result = user_collection.update_one(
            {"_id": user_id},  
            {"$set": {"subscription_id": new_subscription}} 
        )
        
        if result.matched_count == 0:
            return jsonify({"error": "User not found"}), 404
        elif result.modified_count == 0:
            print("No changes were made; subscription_id was already set to the same value.")
            return jsonify({"message": f"Subscription already matches value entered ."}), 200
        else:
            print("Subscription updated successfully.")
            return jsonify({"message": f"Subscription updated successfully."}), 200
    except Exception as e:
        print(f"An error occurred: {e}")