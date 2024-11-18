from flask import Blueprint, jsonify, request
from app.services.subscription_services import edit_subscription

subscription_bp = Blueprint('subscription', __name__, url_prefix='/subscription')

@subscription_bp.route('/manage', methods=['POST'])
def manage_subscription_endpoint():
    user_id = request.json.get('user_id')
    new_subscription = request.json.get('new_subscription') 

    return edit_subscription(user_id, new_subscription)

@subscription_bp.route('/edit subscription', methods=['POST'])
def edit_subscription_endpoint():
    subscription = request.json.get('subscription') 
    new_subscription = request.json.get('new_subscription')

    return edit_subscription(subscription, new_subscription)