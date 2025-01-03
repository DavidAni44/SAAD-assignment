from app.services.database import user_collection, subscription_collection, media_collection, branch_collection
from flask import request, jsonify


def get_users():
    users = user_collection.find()
    all_users = []
    for user in users:
        all_users.append({"name": user.get("name"), "email": user.get("email"), "subscription_id": user.get("subscription_id")})
    return all_users

def get_media():
    media_list = media_collection.find()
    all_media = {}
    for media in media_list:
        all_media.update({media.get("title"): media.get("genre")})
    return len(all_media)

def get_branches():
    branches = branch_collection.find()
    all_branches = []
    for branch in branches:
        all_branches.append({"name": branch.get("name")})
    return all_branches

def get_media_by_branch():
    branches = branch_collection.find()
    result = []

    for branch in branches:
        branch_info = {
            "name": branch["name"],
        }
        
        media_info = branch.get("media", [])
        branch_result = {
            "branch": branch_info,
            "media": media_info
        }
        
        result.append(branch_result)
        
    return result
    
    






