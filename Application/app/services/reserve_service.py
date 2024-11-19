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


#Implemented Observer pattern for notifying users if their reserved media becomes avaliable
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

def notify_observers(media_id):
    for observer in observers:
        observer(media_id)

def return_media(media_id):
    try:
        media_id = ObjectId(media_id)
        print(f"Media with ID {media_id} has been returned.")
        notify_observers(media_id)
        return {"message": f"Media with ID {media_id} has been returned."}, 200
    except Exception as e:
        return {"error": f"Error handling media return: {str(e)}"}, 400

def user_observer_factory(user_id, media_id):
    def observer(returned_media_id):
        if str(returned_media_id) != str(media_id):  # Match specific media ID
            return
        user = user_collection.find_one({"_id": user_id})
        if user:
            notify_user(user, returned_media_id)
    return observer

def notify_user(user, media_id):
    user_email = user.get('email')
    if not user_email:
        print(f"User {user['_id']} does not have an email address.")
        return

    subject = "Media Now Available"
    body = f"""Hello {user['name']},

The media with ID {media_id} that you reserved is now available for checkout.

Thank you."""
    try:
        send_email(user_email, subject, body)
        print(f"Email notification sent to {user_email}")
    except Exception as e:
        print(f"Failed to send email to {user_email}: {e}")

def send_email(to_email, subject, body):
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

def return_staged():
    for user in user_collection.find({"reserved_media": {"$exists": True, "$ne": []}}):
        user_id = user["_id"]
        for media_id in user["reserved_media"]:
            add_observer(user_observer_factory(user_id, media_id))

    media_id_to_return = "67339ffc268d647e800b6fdc"  # Example media ID to return
    response, status = return_media(media_id_to_return)
    return jsonify(response), status
