from flask import Flask, request, jsonify
from app.services.database import user_collection, media_collection

def procure_media(media_details):
    media_collection.insert_one(media_details)
    return jsonify({"message": "Media procured successfully."}), 200