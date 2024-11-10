from flask import Flask, render_template, redirect, request, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os
import smtplib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


app = Flask(__name__, template_folder='templates', static_folder='static')

secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    print("No secret key found. Using fallback key.")
    secret_key = "supersecretkey1234"  # Use a fallback key (only for development)

app.secret_key = secret_key

# MongoDB connection
client = MongoClient(f'mongodb+srv://{os.getenv("DBUSERNAME")}:{os.getenv("DBPASSWORD")}@saaddatabase.8f32e.mongodb.net/?retryWrites=true&w=majority&appName=SAADdatabase')
db = client["AMLdb"]
media_collection = db["Media Data"]  # Media collection
user_collection = db["User Data"]   # Users collection

@app.route('/')

def index():
    # Retrieve all media documents from MongoDB
    media_items = list(media_collection.find())
    # In the Python backend, before passing to the template
    media_items = list(media_collection.find())

# Convert ObjectId to string in Python before passing to template
    for item in media_items:
        item['_id'] = str(item['_id'])

    return render_template('index.html', media_items=media_items)

# Option 1: View All Media
@app.route('/view_all_media')
def view_all_media():
    media_items = list(media_collection.find())

    # Convert ObjectId to string before passing to template
    for item in media_items:
        item['_id'] = str(item['_id'])  # Convert ObjectId to string

    return render_template('view_all_media.html', media_items=media_items)


# Option 2: View All Users and Search by Name
@app.route('/view_all_users', methods=['GET', 'POST'])
def view_all_users():
    if request.method == 'POST':
        name = request.form.get('name')
        user = user_collection.find_one({"name": name})
        if user:
            return render_template('view_user.html', user=user)
        else:
            flash("User not found")
            return redirect(url_for('view_all_users'))
    
    users = list(user_collection.find())
    return render_template('view_all_users.html', users=users)

# Option 3: Add Media
@app.route('/add_media', methods=['GET', 'POST'])
def add_media():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        status = request.form['status']
        media_type = request.form['type']
        description = request.form['description']
        year_published = request.form['year_published']

        media_item = {
            "title": title,
            "author": author,
            "genre": genre,
            "status": status,
            "type": media_type,
            "description": description,
            "year_published": year_published
        }

        media_collection.insert_one(media_item)
        flash(f"{title} has been added to the collection.")
        return redirect(url_for('index'))

    return render_template('add_media.html')

# Option 4: Delete Media
@app.route('/delete_media/<media_id>', methods=['POST'])
def delete_media(media_id):
    media_collection.delete_one({"_id": ObjectId(media_id)})
    flash("Media has been deleted.")
    return redirect(url_for('view_all_media'))  # or redirect to any other page


@app.route('/edit_media/<media_id>', methods=['GET', 'POST'])
def edit_media(media_id):
    # Convert media_id from string to ObjectId
    media_item = media_collection.find_one({"_id": ObjectId(media_id)})

    if not media_item:
        flash("Media not found!")
        return redirect(url_for('view_all_media'))

    if request.method == 'POST':
        # Update the media item with the form data
        media_item['title'] = request.form['title']
        media_item['author'] = request.form['author']
        media_item['genre'] = request.form['genre']
        media_item['status'] = request.form['status']
        media_item['type'] = request.form['type']
        media_item['description'] = request.form['description']
        media_item['year_published'] = request.form['year_published']
        
        # Update the media in the collection
        media_collection.update_one({"_id": ObjectId(media_id)}, {"$set": media_item})
        flash(f"{media_item['title']} has been updated.")
        return redirect(url_for('view_all_media'))

    return render_template('edit_media.html', media_item=media_item)


# Option 6: Delete User
@app.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    user_collection.delete_one({"_id": ObjectId(user_id)})
    flash("User has been deleted.")
    return redirect(url_for('view_all_users'))

# Option 7: Edit User
@app.route('/edit_user/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = user_collection.find_one({"_id": ObjectId(user_id)})

    if request.method == 'POST':
        user['name'] = request.form['name']
        user['email'] = request.form['email']
        user['address'] = request.form['address']
        user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": user})
        flash(f"{user['name']} has been updated.")
        return redirect(url_for('view_all_users'))

    return render_template('edit_user.html', user=user)

# Option 8: Add New User
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']

        new_user = {
            "name": name,
            "email": email,
            "address": address
        }

        user_collection.insert_one(new_user)
        flash(f"{name} has been added as a new user.")
        return redirect(url_for('index'))

    return render_template('add_user.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
