from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient(f'mongodb+srv://{os.getenv("DBUSERNAME")}:{os.getenv("DBPASSWORD")}@your-cluster-url')
db = client["AMLdb"]
media_collection = db["Media Data"]

@app.route('/reserve_media', methods=['POST'])
def reserve_media():
    user_id = request.json.get('user_id')
    media_id = request.json.get('media_id')
    
    # Check if media is available
    media = media_collection.find_one({"_id": media_id, "availability": True})
    if not media:
        return jsonify({"error": "Media not available"}), 400
    
    # Reserve media
    media_collection.update_one({"_id": media_id}, {"$set": {"availability": False}})
    
    return jsonify({"message": f"Successfully reserved media: {media['title']}"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
