from app.services.database import user_collection, subscription_collection, media_collection
from flask import request, jsonify


def get_users():
    users = user_collection.find()
    all_users = {}
    for user in users:
        all_users.update({user.get("name"): user.get("address")})
    return len(all_users)

def get_media():
    media_list = media_collection.find()
    all_media = {}
    for media in media_list:
        all_media.update({media.get("title"): media.get("genre")})
    return len(all_media)



