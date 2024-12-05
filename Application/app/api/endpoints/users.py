from flask import Blueprint, jsonify, request
from app.services.users_services import get_user_by_id
from app.services.monitor_system import get_users
import requests
from datetime import datetime

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    print(user_id)
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


@user_bp.route('/all_users', methods=['GET'])
def return_all_users():
    users = get_users()
    return jsonify(users), 200


def ping_endpoint():
    ping_logs = []
    try:
        response = requests.get('http://127.0.0.1:5000/api/users/ping')
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "status": response.status_code
        }
        ping_logs.append(log_entry)  # Add log to the global list
        return log_entry  # Return the latest log entry (optional, for manual calls)
    except requests.RequestException:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "status": "Error"
        }
        ping_logs.append(log_entry)
    return ping_logs  # Return the latest log entry (optional, for manual calls)


@user_bp.route('/ping_logs', methods=['GET'])
def get_ping_logs():
    ping = ping_endpoint()
    return jsonify(ping), 200

@user_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "Ping successful"}), 200