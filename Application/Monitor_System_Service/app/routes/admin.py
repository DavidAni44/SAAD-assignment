from flask import Blueprint, jsonify, request
from app.services.subscription_services import edit_subscription, get_subscription, get_users_with_subscriptions


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/get_subs', methods=['GET'])
def get_subs():
    subs = get_users_with_subscriptions()
    return jsonify(subs), 200
