from app.services.database import user_collection, media_collection
from flask import request, jsonify

def reserve_media(user_id, media_id):
    # Check if media is available
    media = media_collection.find_one({"_id": media_id, "availability": True})
    if not media:
        return jsonify({"error": "Media not available"}), 400

    # Update media to mark as reserved
    media_collection.update_one({"_id": media_id}, {"$set": {"availability": False}})

    return jsonify({"message": f"Successfully reserved media: {media['title']}"}), 200