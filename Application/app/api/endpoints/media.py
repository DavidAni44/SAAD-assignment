from flask import Blueprint, jsonify, request
from app.services.borrow_service import borrow_media
from app.services.media_procurement_service import procure_media
from app.services.reserve_service import reserve_media

media_bp = Blueprint('media', __name__, url_prefix='/media')

@media_bp.route('/test', methods=['GET'])
def test_media():
    return jsonify({"message": "Media route is working!"})

@media_bp.route('/borrow', methods=['POST'])
def borrow_media_endpoint():
    user_id = request.json.get('user_id')
    media_id = request.json.get('media_id')

    return borrow_media(user_id, media_id)

@media_bp.route('/procure', methods=['POST'])
def procure_media_endpoint():
    media_details = request.get_json()  

    return procure_media(media_details)

@media_bp.route('/reserve', methods=['POST'])
def reserve_media_endpoint():
    user_id = request.json.get('user_id')
    media_id = request.json.get('media_id')

    return reserve_media(user_id, media_id)