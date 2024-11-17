from datetime import datetime, timedelta
from flask import jsonify
from bson import ObjectId
from app.services.database import user_collection, media_collection, transaction_collection, branch_collection


def borrow_media(user_id, media_id,delivery_choice):

    
    media_id = ObjectId(media_id)
    user = user_collection.find_one({"_id": user_id})

    if check_media_avaliable(user,media_id):
        pass
    else:
        return jsonify({"error": "Media not available at user's home branch"}), 400

    update_branch_stock(user,media_id)
    update_user_media_borrowed(user_id,media_id)
    send_user_email(user,media_id) #doesnt work yet
    create_transaction(user,media_id, delivery_choice)
    return jsonify({"message": f"Successfully borrowed media: {media_id}"}), 200



def create_transaction(user,media_id, delivery_choice):
    borrowed_date = datetime.now()
    due_date = borrowed_date + timedelta(days=14)
    media = media_collection.find_one({"_id": media_id}) 
    transaction = {
        "user_id": user.get("user_id"),
        "media_id": str(media_id),
        "branch_id": user.get("branch_id"),
        "borrowed_date": borrowed_date.strftime("%Y-%m-%d"),
        "due_date": due_date.strftime("%Y-%m-%d"),
        "return_date": None,
        "returned": False,
        "Late return fee per day": (media_collection.find_one({"_id": media_id})).get("late_return_fee_per_day") ,   
        "delivery type": delivery_choice
   
    }
    if delivery_choice == "Home Delivery":
        transaction["delivery address"] = user.get("address")  
        transaction["postage"] = 3.99
        transaction["payment method"] = user.get("payment_method") 
    transaction_collection.insert_one(transaction)
    print(transaction)


def send_user_email(user,media_id):
    user.get("email")
    #this doenst work yet



def update_user_media_borrowed(user_id,media_id):
    user_collection.update_one({"_id": user_id}, {"$push": {"borrowed_media": str(media_id)}})



def update_branch_stock(user,media_id):
    branch_collection.update_one(
        {"_id": user.get("branch_id"), "media.media_id": str(media_id)},
        {"$inc": {"media.$.available_copies": -1}}
    )



def check_media_avaliable(user,media_id):
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
    return branch