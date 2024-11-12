
from bson import ObjectId
from flask import request, jsonify

def borrow_media(user_id, media_id):
    from app.services.database import user_collection, media_collection

    media_id = ObjectId(media_id)

    media = media_collection.find_one({"_id": media_id, "status": "available"})
    if not media:
        return jsonify({"error": "Media not available"}), 400
    
    # Update media availability
    media_collection.update_one({"_id": media_id}, {"$set": {"status": "borrowed"}})
    
    # Update user borrowed media
    user_collection.update_one({"_id": user_id}, {"$push": {"borrowed_media": media_id}})
    
    return jsonify({"message": f"Successfully borrowed media: {media['title']}"}), 200
