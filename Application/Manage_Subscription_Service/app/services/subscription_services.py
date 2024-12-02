from app.services.database import user_collection, media_collection, transaction_collection, branch_collection, library_collection, subscription_collection
from flask import request, jsonify
from bson import json_util
from bson import ObjectId

def edit_subscription(user_id, new_subscription):

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
    
    

# get all subscriptions
def get_subscription():
    subscriptions = subscription_collection.find()
    all_subscriptions = []
    for subscription in subscriptions:
        all_subscriptions.append({"_id": json_util.dumps(subscription.get("_id")), "subscription_name": subscription.get("subscription_name"), "subscription_price_per_month": subscription.get("subscription_price_per_month")})
    return all_subscriptions



def get_users_with_subscriptions():
    # Fetch all users from the user collection
    users = user_collection.find()
    
    # Create a list to store user data with subscription info
    user_subscription_data = []
    
    for user in users:
        # Get the subscription ID from the user
        subscription_id = user.get("subscription_id")
        
        # Fetch the subscription info based on the subscription ID
        subscription = subscription_collection.find_one({"_id": ObjectId(subscription_id)})
        
        # Combine user and subscription data
        if subscription:
            combined_data = {
                "user_id": str(user["_id"]),
                "name": user.get("name"),
                "email": user.get("email"),
                "subscription_id": str(subscription["_id"]),
                "subscription_name": subscription.get("subscription_name"),
                "subscription_price_per_month": subscription.get("subscription_price_per_month"),
            }
        else:
            # If no subscription is found, return user info without subscription details
            combined_data = {
                "user_id": str(user["_id"]),
                "name": user.get("name"),
                "email": user.get("email"),
                "subscription_id": None,
                "subscription_name": None,
                "subscription_price_per_month": None,
            }
        
        user_subscription_data.append(combined_data)
    
    return user_subscription_data

    


#create reports for payments recieved 



# create email payload to send mail once subscription is updated 


