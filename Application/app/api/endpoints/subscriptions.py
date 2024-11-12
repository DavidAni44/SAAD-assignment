from flask import Blueprint, jsonify, request
from app.services.subscription_services import manage_subscription

subscription_bp = Blueprint('subscription', __name__, url_prefix='/subscription')

@subscription_bp.route('/manage', methods=['POST'])
def manage_subscription_endpoint():
    user_id = request.json.get('user_id')
    action = request.json.get('action') 

    return manage_subscription(user_id, action)