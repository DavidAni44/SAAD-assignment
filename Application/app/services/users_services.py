from app.services.database import user_collection, media_collection, transaction_collection, branch_collection, library_collection
from bson import ObjectId

def get_user_by_id(user_id):
    user = user_collection.find_one({"_id": user_id})
    print(user)
    if user:
        return {"name": user["name"], "email": user["email"]}
    return None
