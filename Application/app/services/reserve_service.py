from app.services.database import user_collection, media_collection, transaction_collection, branch_collection
from flask import  jsonify
 
def get_available_media_by_branch():
    branch_media = {}
    for branch in media_collection.find():
        branch_id = branch.get("_id")
        available_media = [
            item["media_id"]
            for item in branch.get("media", [])
            if item.get("available_copies", 0) > 0  
        ]
        branch_media[branch_id] = available_media
    return branch_media

def get_all_users():
    users = list(user_collection.find())
    return users

def check_media_availability():
    print("Running media availability check...")
    branch_media = get_available_media_by_branch()
    users = get_all_users()
    for user in users:
        branch_id = user.get("branch_id")
        reserved_media = user.get("reserved_media", [])
        if not branch_id or not reserved_media:
            continue  
        available_media_in_branch = branch_media.get(branch_id, [])
        media_matches = [media for media in reserved_media if media in available_media_in_branch]
        if media_matches:
            print(f"User: {user.get('name', 'Unknown')} | Branch: {branch_id}")
            print(f"Matching Media: {media_matches}")


def reserve_media(user_id, media_id):
    media_id = str(media_id)
    user = user_collection.find_one({"_id": user_id})
    if check_media_unavaliable(user,media_id):
        add_to_reserved_media(user,media_id)

    else:
        return jsonify({"error": "Media not found in user's home branch"}), 400



def add_to_reserved_media(user_id,media_id):
    result = user_collection.update_one(
        {"_id": user_id},
        {"$addToSet": {"reserved_media": str(media_id)}} 
    )
    if result.modified_count > 0:
        return jsonify({"message": "Media reserved successfully"}), 200
    else:
        return jsonify({"message": "Media was already reserved"}), 200



def check_media_unavaliable(user,media_id):
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
                "available_copies": {"$eq": 0}  
            }
        }
    })

    return branch


#from apscheduler.schedulers.background import BackgroundScheduler
#scheduler = BackgroundScheduler()

#scheduler.add_job(check_media_availability, "interval", minutes=1)

#scheduler.start()
#print("Scheduler started. Press Ctrl+C to exit.")

#try:
#    while True:
#        pass
#except (KeyboardInterrupt, SystemExit):
#    scheduler.shutdown()
#    print("Scheduler stopped.")

