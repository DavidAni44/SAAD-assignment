from flask import Flask, render_template, redirect, request, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "a_random_fallback_secret_key")  # Replace with a real secret key in production

# MongoDB connection
client = MongoClient(f'mongodb+srv://{os.getenv("DBUSERNAME")}:{os.getenv("DBPASSWORD")}@saaddatabase.8f32e.mongodb.net/?retryWrites=true&w=majority&appName=SAADdatabase')
db = client["AMLdb"]
user_collection = db["User Data"]
media_collection = db["Media Data"]

# Hardcoded user ID
hardcoded_user_id = "6731ff43268d647e801147bf"

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# View Account Information (for hardcoded user)
@app.route('/account')
def account():
    user = user_collection.find_one({"_id": hardcoded_user_id})
    return render_template('account.html', user=user)

# Borrow Media (for hardcoded user)
@app.route('/borrow_media', methods=['GET', 'POST'])
def borrow_media():
    user = user_collection.find_one({"_id": ObjectId(hardcoded_user_id)})
    

    if request.method == 'POST':
        media_id = request.form['media_id']
        media = media_collection.find_one({"_id": ObjectId(media_id)})

        if media and media.get('availability', False):
            # Update borrowed_media in user document
            user_collection.update_one(
                {"_id": ObjectId(hardcoded_user_id)},
                {"$push": {"borrowed_media": {"_id": media["_id"], "title": media["title"]}}}
            )
            # Update media availability
            media_collection.update_one(
                {"_id": ObjectId(media_id)},
                {"$set": {"availability": False}}
            )
            flash(f"You've successfully borrowed {media['title']}", 'success')
            return redirect(url_for('borrow_media'))

        flash("Media is not available or doesn't exist.", 'error')
        return redirect(url_for('borrow_media'))

    available_media = media_collection.find({"availability": True})
    return render_template('borrow_media.html', available_media=available_media, user=user)

# Return Media (for hardcoded user)
@app.route('/return_media/<media_id>', methods=['GET'])
def return_media(media_id):
    user = user_collection.find_one({"_id": ObjectId(hardcoded_user_id)})

    # Find the media item in user's borrowed_media
    media = media_collection.find_one({"_id": ObjectId(media_id)})
    if media:
        # Remove media from user's borrowed list
        user_collection.update_one(
            {"_id": ObjectId(hardcoded_user_id)},
            {"$pull": {"borrowed_media": {"_id": media["_id"], "title": media["title"]}}}
        )
        # Set media availability to True
        media_collection.update_one(
            {"_id": ObjectId(media_id)},
            {"$set": {"availability": True}}
        )
        flash(f"You've successfully returned {media['title']}.", 'success')
    else:
        flash("Media not found.", 'error')

    return redirect(url_for('account'))

# Admin Dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    users = user_collection.find()
    return render_template('admin_dashboard.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
