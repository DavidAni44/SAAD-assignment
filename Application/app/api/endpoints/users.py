from flask import Blueprint, jsonify, request
from app.services.users_services import get_user_by_id

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    print(user_id)
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200