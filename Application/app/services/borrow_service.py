from app.services.database import user_collection, media_collection
from flask import request, jsonify

def borrow_media():
    user_id = request.json.get('user_id')
    media_id = request.json.get('media_id')
    
    # Check if media is available
    media = media_collection.find_one({"_id": media_id, "availability": True})
    if not media:
        return jsonify({"error": "Media not available"}), 400
    
    # Update media availability
    media_collection.update_one({"_id": media_id}, {"$set": {"availability": False}})
    
    # Update user borrowed media
    user_collection.update_one({"_id": user_id}, {"$push": {"borrowed_media": media_id}})
    
    return jsonify({"message": f"Successfully borrowed media: {media['title']}"}), 200
