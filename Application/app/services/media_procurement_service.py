from bson import ObjectId
from flask import  jsonify
from app.services.database import user_collection, media_collection, transaction_collection, branch_collection, library_collection,purchase_order_collection
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def procure_media(media_to_order,branch_to_deliver_to,quantity_to_order,delivery_date):
    print(media_to_order)
    print(branch_to_deliver_to)
    order_id = create_order(media_to_order,branch_to_deliver_to,quantity_to_order,delivery_date) 
    prepare_email(branch_to_deliver_to,quantity_to_order,media_to_order,order_id,delivery_date)
    return jsonify({"message": "Media procured successfully."}), 200

def create_order(media_to_order,branch_to_deliver_to,quantity_to_order,delivery_date):


    purchase_order = {
        "media_to_order": (media_collection.find_one({"_id": ObjectId(media_to_order)})).get("_id"),  #not working
        "branch_to_deliverto": branch_to_deliver_to,
        "quantity_to_order": quantity_to_order,
        "delivery_date": delivery_date,
        "supplier": (media_collection.find_one({"_id": ObjectId(media_to_order)})).get("vendor_name"),
        "supplier_contact": (media_collection.find_one({"_id": ObjectId(media_to_order)})).get("vendor_contact"),
        "price_per_item": (media_collection.find_one({"_id": ObjectId(media_to_order)})).get("price_per_item"),
        "total_price": (media_collection.find_one({"_id": ObjectId(media_to_order)})).get("price_per_item")*quantity_to_order,
        "status": "Purchase Order Sent To Supplier",
    }
    
    purchase_order_collection.insert_one(purchase_order)
    print (purchase_order)

    return purchase_order.get('_id')


def get_branch_email(branch_to_deliver_to):
    branch = branch_collection.find_one({'_id': branch_to_deliver_to})
    email = branch.get('branch_email', 'Email not available')
    return email



def prepare_email(branch_to_deliver_to,quantity_to_order,media_to_order,order_id,delivery_date):
    print("Preparing Email")
    subject = "Media Order From ALM: "+ str(order_id)
    body = "Dear Vendor, \n\n This is an order for " + str(quantity_to_order) + " " + \
       (media_collection.find_one({"_id": ObjectId(media_to_order)})).get("title") + \
       "\n\nTo our branch " + branch_collection.find_one({'_id': branch_to_deliver_to}).get('name') + \
       "\n\nFor delivery date: " + delivery_date + " \n\nKind Regards ALM"

    email = get_branch_email(branch_to_deliver_to)
    send_email(subject, body, email)


def send_email(subject,body,email):
    print("sending email")
    smtpServer = "smtp.gmail.com"
    smtpPort = 587
    senderEmail = "xclwright@gmail.com"
    senderPassword = "ijmf mqtd egvo erjc"  

    email = "xclwright@outlook.com" #"philandy83@gmail.com" # change to vendor and branch emails
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
    
    







