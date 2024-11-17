from app.services.database import user_collection, media_collection, transaction_collection, branch_collection
from flask import request, jsonify


def reserve_media(user_id, media_id):
    media_id = str(media_id)
    user = user_collection.find_one({"_id": user_id})
    if check_media_unavaliable(user,media_id):
        add_to_reserved_media(user,media_id)

    else:
        return jsonify({"error": "Media not found in user's home branch"}), 400



def add_to_reserved_media(user_id,media_id):
    result = user_collection.update_one(
        {"_id": user_id},
        {"$addToSet": {"reserved_media": str(media_id)}} 
    )
    if result.modified_count > 0:
        return jsonify({"message": "Media reserved successfully"}), 200
    else:
        return jsonify({"message": "Media was already reserved"}), 200



def check_media_unavaliable(user,media_id):
    home_branch_id = user.get("branch_id")
    if not home_branch_id:
        return jsonify({"error": "User does not have a home branch assigned"}), 400

    branch_data = branch_collection.find_one({"_id": home_branch_id})
    if branch_data is None:
        return jsonify({"error": "Branch not found"}), 404

    branch = branch_collection.find_one({
        "_id": home_branch_id,
        "media": {
            "$elemMatch": {
                "media_id": str(media_id),
                "available_copies": {"$eq": 0}  
            }
        }
    })

    return branch