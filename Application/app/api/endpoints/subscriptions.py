from flask import Blueprint, jsonify, request
from app.services.subscription_services import edit_subscription, get_subscription, get_users_with_subscriptions
from app.services.database import user_collection, subscription_collection
from bson import ObjectId

subscription_bp = Blueprint('subscription', __name__, url_prefix='/subscription')

@subscription_bp.route('/manage', methods=['POST'])
def manage_subscription_endpoint():
    user_id = request.json.get('user_id')
    new_subscription = request.json.get('new_subscription') 

    return edit_subscription(user_id, new_subscription)

@subscription_bp.route('/edit_subscription', methods=['POST'])
def edit_subscription_endpoint():
    subscription = request.json.get('subscription') 
    new_subscription = request.json.get('new_subscription')

    return edit_subscription(subscription, new_subscription)

@subscription_bp.route('/get_all', methods=['GET'])
def get_all_subscriptions():
    return jsonify(get_subscription()), 200


@subscription_bp.route('/get_subs', methods=['GET'])
def get_subs():
    page = request.args.get('page', default=1, type=int)  # Default page is 1
    limit = request.args.get('limit', default=10, type=int)  # Default limit is 10

    subs = get_users_with_subscriptions(page=page, limit=limit)
    return jsonify(subs), 200


@subscription_bp.route('/update_user_subscription/<user_id>', methods=['POST'])
def update_user_subscription(user_id):
    try:
        # Parse the JSON data from the request
        data = request.json
        new_subscription_id = data.get("subscription_id")

        # Validate the subscription ID
        if not new_subscription_id:
            return jsonify({"error": "No subscription ID provided"}), 400

        # Update the user's subscription in the database
        result = user_collection.update_one(
            {"_id": (user_id)},  # Filter by user ID
            {"$set": {"subscription_id": new_subscription_id}}  # Update subscription ID
        )

        if result.matched_count == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "Subscription updated successfully"}), 200
    except Exception as e:
        print(f"Error updating subscription: {e}")
        return jsonify({"error": "An error occurred"}), 500
    
    
@subscription_bp.route('/update', methods=['POST'])
def update_subscription_price():
    data = request.json
    subscription_id = data.get('subscription_id')  # Subscription ID
    new_price = data.get('new_price')             # New subscription price

    if not subscription_id or not new_price:
        return jsonify({"error": "Missing subscription ID or new price"}), 400

    print(f"Received subscription_id: {subscription_id}, new_price: {new_price}")

    result = subscription_collection.update_one(
        {"subscription_id": subscription_id},
        {"$set": {"subscription_price_per_month": float(new_price)}}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Subscription not found"}), 404

    return jsonify({"message": "Subscription price updated successfully"}), 200
