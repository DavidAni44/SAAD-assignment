from flask import Blueprint, jsonify, request
from app.services.borrow_service import borrow_media
from app.services.media_procurement_service import procure_media, track_order, edit_order_status
from app.services.reserve_service import reserve_media, return_staged
from app.services.monitor_system import get_media, get_branches, get_media_by_branch
from app.services.report_service import export_as, report_selection

media_bp = Blueprint('media', __name__, url_prefix='/media')



@media_bp.route('/borrow', methods=['POST'])
def borrow_media_endpoint():
    user_id = request.json.get('user_id')
    media_id = request.json.get('media_id')
    delivery_choice = request.json.get('delivery_choice')
    borrow_until = request.json.get('borrow_until')
    return borrow_media(user_id, media_id, delivery_choice,borrow_until)

@media_bp.route('/procure', methods=['POST'])
def procure_media_endpoint():
    quantity_to_order = request.json.get("quantity_to_order")  
    branch_to_deliver_to = request.json.get("branch_to_deliver_to")  
    media_to_order = request.json.get("media_to_order")  
    delivery_date = request.json.get("delivery_date")
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

@media_bp.route('/all_branches', methods=['GET'])
def get_all_branches():
    branch = get_branches()
    return jsonify(branch), 200

@media_bp.route('/all_branch_media', methods=['GET'])
def get_all_branch_media():
    branch = get_media_by_branch()
    return jsonify(branch), 200

@media_bp.route('/mediareturned', methods=['POST'])
def return_staged_endpoint():
    branch_id = request.json.get('branch_id')
    media_id = request.json.get('media_id')
    return return_staged(branch_id, media_id)


@media_bp.route('/track_order', methods=['GET'])
def track_order_endpoint():
    PO = request.json.get('PO')
    order_location = track_order(PO)
    return jsonify(order_location), 200

@media_bp.route('/edit_order', methods=['POST'])
def edit_order_endpoint():
    PO = request.json.get('PO')
    new_status = request.json.get('new_status')
    updated_order = edit_order_status(PO,new_status)
    return str(updated_order), 200