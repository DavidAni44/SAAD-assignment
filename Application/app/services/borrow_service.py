from datetime import datetime, timedelta
from flask import jsonify
from bson import ObjectId

def borrow_media(user_id, media_id):
    from app.services.database import user_collection, media_collection, transaction_collection, branch_collection

    try:
        media_id = ObjectId(media_id)
    except Exception as e:
        return jsonify({"error": "Invalid media_id format"}), 400

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
                "available_copies": {"$gt": 0}
            }
        }
    })

    if branch:
        pass
    else:
        return jsonify({"error": "Media not available at user's home branch"}), 400

    branch_collection.update_one(
        {"_id": home_branch_id, "media.media_id": str(media_id)},
        {"$inc": {"media.$.available_copies": -1}}
    )

    user_collection.update_one({"_id": user_id}, {"$push": {"borrowed_media": str(media_id)}})

    borrowed_date = datetime.now()
    due_date = borrowed_date + timedelta(days=14)
    transaction = {
        "user_id": user_id,
        "media_id": str(media_id),
        "branch_id": home_branch_id,
        "borrowed_date": borrowed_date.strftime("%Y-%m-%d"),
        "due_date": due_date.strftime("%Y-%m-%d"),
        "return_date": None
    }
    transaction_collection.insert_one(transaction)

    media = media_collection.find_one({"_id": ObjectId(media_id)})
    if not media:
        return jsonify({"error": "Media document not found"}), 404

    return jsonify({"message": f"Successfully borrowed media: {media['title']}"}), 200

