from flask import Blueprint, jsonify, request
from app.services.subscription_services import edit_subscription, get_subscription, get_users_with_subscriptions


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/get_subs', methods=['GET'])
def get_subs():
    subs = get_users_with_subscriptions()
    return jsonify(subs), 200


@admin_bp.route('/report', methods=['POST'])
def report_endpoint():
    report_choice = request.json.get('report')
    format_type = request.json.get('export')

    report_data,report_name = report_selection(report_choice)
    export_as(format_type,report_data,report_name)

    return str(report_data), 200