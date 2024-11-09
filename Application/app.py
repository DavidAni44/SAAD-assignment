from flask import Flask, render_template, redirect, request, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import os
import smtplib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.getenv("SECRET_KEY")

# MongoDB connection
client = MongoClient(f'mongodb+srv://{os.getenv("DBUSERNAME")}:{os.getenv("DBPASSWORD")}@saaddatabase.8f32e.mongodb.net/?retryWrites=true&w=majority&appName=SAADdatabase')
db = client["LibraryDB"]
collection = db["Media"]

@app.route('/')
def index():
    # Retrieve all media documents from MongoDB
    media_items = list(collection.find())
    return render_template('index.html', media_items=media_items)

@app.route('/borrow/<media_id>', methods=['GET', 'POST'])
def borrow_media(media_id):
    media_item = collection.find_one({"_id": ObjectId(media_id)})

    if media_item and media_item.get("status") == "available":
        if request.method == 'POST':
            # Retrieve user data and choices from the form
            user_email = request.form.get('email')
            user_phone = request.form.get('phone')
            pickup_option = request.form.get('pickup_option')
            due_date = datetime.now() + timedelta(days=14)

            # Update media status to 'borrowed' in MongoDB
            collection.update_one(
                {"_id": ObjectId(media_id)},
                {"$set": {"status": "borrowed", "due_date": due_date}}
            )

            # Send confirmation
            send_confirmation(user_email, user_phone, media_item["title"], due_date, pickup_option)

            flash("Borrow request confirmed. A confirmation has been sent via email/SMS.")
            return redirect(url_for('index'))

        return render_template('borrow.html', media_item=media_item)
    else:
        flash("The media item is currently unavailable.")
        return redirect(url_for('index'))

def send_confirmation(email, phone, title, due_date, pickup_option):
    confirmation_message = f"Thank you for borrowing '{title}'.\nDue Date: {due_date.strftime('%Y-%m-%d')}\nPickup Option: {pickup_option}"

    # Send email
    send_email(email, "Media Borrowing Confirmation", confirmation_message)

    # Send SMS (if phone number provided and using an SMS provider like Twilio)
    if phone:
        send_sms(phone, confirmation_message)

def send_email(to_email, subject, message):
    smtp_server = "smtp.your-email-provider.com"
    smtp_port = 587
    from_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(from_email, password)
        email_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(from_email, to_email, email_message)

def send_sms(to_phone, message):
    # Placeholder function - Integrate with SMS service provider like Twilio
    pass  # Add SMS API integration code here

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)