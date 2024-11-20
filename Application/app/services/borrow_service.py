from datetime import datetime, timedelta
from flask import jsonify
from bson import ObjectId
from app.services.database import user_collection, media_collection, transaction_collection, branch_collection
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def borrow_media(user_id, media_id,delivery_choice,borrow_until ):
    media_id = ObjectId(media_id)
    user = user_collection.find_one({"_id": user_id})
    if check_media_avaliable(user,media_id):
        pass
    else:
        return jsonify({"error": "Media not available at user's home branch"}), 400

    update_branch_stock(user,media_id)
    update_user_media_borrowed(user_id,media_id)
    transaction_id = create_transaction(user,media_id, delivery_choice,borrow_until)
    print(transaction_id)
    subject,body,email = prepare_email(transaction_id,user)
    send_user_email(subject,body,email)
    return jsonify({"message": f"Successfully borrowed media: {media_id}"}), 200


def create_transaction(user,media_id, delivery_choice,borrow_until):
    date = datetime.now()
    date = date.date().strftime("%Y-%m-%d")
    transaction = {
        "user_id": user.get("_id"),  
        "media_id": str(media_id),
        "branch_id": user.get("branch_id"),
        "borrowed_date": date,
        "due_date": borrow_until,
        "return_date": None,
        "returned": False, 
        "delivery_type": delivery_choice
   
    }
    if delivery_choice == "Home Delivery":
        transaction["delivery_address"] = user.get("address")  
        transaction["postage"] = "standard",3.99
        transaction["payment_method"] = user.get("payment_method") 
    transaction_collection.insert_one(transaction)
    print(transaction)
    return transaction.get('_id')
 

def prepare_email(transaction_id,user):
    transaction = transaction_collection.find_one({"_id": ObjectId(transaction_id)}) 
    media = media_collection.find_one({"_id": ObjectId(transaction.get("media_id"))}) 
    subject = "Media Borrowed: " + transaction.get("media_id")
    body = "Dear "+ user.get("name") + "\n"  + "You have borrowed: " + str(media.get("title")) + \
    "\n" + "From: " + str(transaction.get("borrowed_date")) + "\n" + "Until: " + str(transaction.get("due_date")) + "\n" + \
    "Late Return Fee Per Day: " + str(media.get("late_return_fee_per_day")) + "\n" + "Kind Regards\n" + "ALM"
    email = user.get("email")
    return subject,body,email


def send_user_email(subject,body,email):
    smtpServer = "smtp.gmail.com"
    smtpPort = 587
    senderEmail = "xclwright@gmail.com" # ALM's email
    senderPassword = "ijmf mqtd egvo erjc"  
    email = "xclwright@outlook.com" # "philandy83@gmail.com" Davids Test #change to user get email
    message = MIMEMultipart()
    message["From"] = senderEmail
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(str(body), "plain"))

    try:
        server = smtplib.SMTP(smtpServer, smtpPort)
        server.starttls()

        server.login(senderEmail, senderPassword)

        server.sendmail(senderEmail, email, message.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        server.quit()




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