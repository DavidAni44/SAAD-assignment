from flask import Blueprint, jsonify, request
from app.services.borrow_service import borrow_media
from app.services.media_procurement_service import procure_media
from app.services.reserve_service import reserve_media
from app.services.monitor_system import get_media

media_bp = Blueprint('media', __name__, url_prefix='/media')

@media_bp.route('/test', methods=['GET'])
def test_media():
    return jsonify({"message": "Media route is working!"})

@media_bp.route('/borrow', methods=['POST'])
def borrow_media_endpoint():
    user_id = request.json.get('user_id')
    media_id = request.json.get('media_id')
    delivery_choice = request.json.get('delivery_choice')
    return borrow_media(user_id, media_id, delivery_choice)

@media_bp.route('/procure', methods=['POST'])
def procure_media_endpoint():
    quantity_to_order = request.json.get("quantity_to_order")  
    branch_to_deliver_to = request.json.get("branch_to_deliver_to")  
    media_to_order = request.json.get("media_to_order")  
    delivery_date = request.json.get("media_to_order")
    return procure_media(media_to_order,branch_to_deliver_to,quantity_to_order,delivery_date)

@media_bp.route('/reserve', methods=['POST'])
def reserve_media_endpoint():
    user_id = request.json.get('user_id')
    media_id = request.json.get('media_id')

    return reserve_media(user_id, media_id)

@media_bp.route('/all_media', methods=['GET'])
def get_all_media():
    media = get_media()
    return jsonify(media), 200