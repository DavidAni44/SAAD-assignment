from bson import ObjectId
from app.services.database import user_collection, media_collection, transaction_collection, branch_collection
from flask import  jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def reserve_media(user_id, media_id):
    media_id = str(media_id)
    user = user_collection.find_one({"_id": user_id})
    if check_media_unavaliable(user,media_id):
        response, status = add_to_reserved_media(user,media_id)
        return response, status

    else:
        return jsonify({"error": "Media not found in user's home branch"}), 400



def add_to_reserved_media(user_id, media_id):

    result = user_collection.update_one(
        {"_id":str(user_id.get('_id'))},  
        {"$addToSet": {"reserved_media": str(media_id)}}  
    )

    if result.matched_count == 0:
        return "User not found", 404
    elif result.modified_count == 0:
        return "Media was already reserved", 200
    else:
        return "Media reserved successfully", 200


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


    #return jsonify({"message": "Media available"}), 200
    return branch

# Implemented Observer pattern for notifying users if their reserved media becomes available in their home branch
observers = []

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "xclwright@gmail.com"
EMAIL_PASSWORD = "ijmf mqtd egvo erjc"

def add_observer(observer):
    if observer not in observers:
        observers.append(observer)

def remove_observer(observer):
    if observer in observers:
        observers.remove(observer)

def notify_observers(media_id, branch_id):
    for observer in observers:
        observer(media_id, branch_id)

def return_media(media_id, branch_id):
    try:
        media_id = str(ObjectId(media_id))  
        print(f"Media with ID {media_id} has been returned to branch {branch_id}.")
        notify_observers(media_id, branch_id)
        return {"message": f"Media with ID {media_id} has been returned to branch {branch_id}."}, 200
    except Exception as e:
        return {"error": f"Error handling media return: {str(e)}"}, 400

def user_observer_factory(user_id, media_id):
 
    def observer(returned_media_id, returned_branch_id):
        if str(returned_media_id) != str(media_id): 
            return
        user = user_collection.find_one({"_id": user_id})
        if user and user.get("branch_id") == returned_branch_id: 
            notify_user(user, returned_media_id)
    return observer

def notify_user(user, media_id):
    user_email = user.get('email')
    if not user_email:
        print(f"User {user['_id']} does not have an email address.")
        return

    subject = "Media Now Available"
    body = f"""Hello {user['name']},

The media with ID {media_id} that you reserved is now available at your home branch.

Thank you."""
    try:
        send_email(user_email, subject, body)
        print(f"Email notification sent to {user_email}")
    except Exception as e:
        print(f"Failed to send email to {user_email}: {e}")

def send_email(to_email, subject, body):
    to_email = "xclwright@outlook.com"
    message = MIMEMultipart()
    message["From"] = EMAIL_ADDRESS
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, message.as_string())
    except Exception as e:
        print(f"SMTP error occurred: {e}")

def return_staged(branch_id, media):

    for user in user_collection.find({"reserved_media": {"$exists": True, "$ne": []}}):
        user_id = user["_id"]
        for media_id in user["reserved_media"]:
            add_observer(user_observer_factory(user_id, media_id))

    response, status = return_media(media, branch_id)
    return jsonify(response), status
