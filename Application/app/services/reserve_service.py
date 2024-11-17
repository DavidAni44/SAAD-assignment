from app.services.database import user_collection, media_collection, transaction_collection, branch_collection
from flask import request, jsonify

def reserve_media(user_id, media_id):
    media_id = str(media_id)
    user = user_collection.find_one({"_id": user_id})
    if not user:
        return jsonify({"error": "User not found"}), 404

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

    if branch:
        result = user_collection.update_one(
            {"_id": user_id},
            {"$addToSet": {"reserved_media": str(media_id)}} 
        )

        if result.modified_count > 0:
            return jsonify({"message": "Media reserved successfully"}), 200
        else:
            return jsonify({"message": "Media was already reserved"}), 200
    else:
        return jsonify({"error": "Media is not available or not found in user's home branch"}), 400
