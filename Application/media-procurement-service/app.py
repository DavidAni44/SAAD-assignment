from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient(f'mongodb+srv://{os.getenv("DBUSERNAME")}:{os.getenv("DBPASSWORD")}@your-cluster-url')
db = client["AMLdb"]
media_collection = db["Media Data"]

@app.route('/procure_media', methods=['POST'])
def procure_media():
    media_details = request.json
    
    # Add media to the procurement collection
    media_collection.insert_one(media_details)
    
    return jsonify({"message": "Media procured successfully."}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)
