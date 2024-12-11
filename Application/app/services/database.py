import os
from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    # MongoDB connection
    client = MongoClient(
        f'mongodb+srv://{os.getenv("DBUSERNAME")}:{os.getenv("DBPASSWORD")}'
        '@saaddatabase.8f32e.mongodb.net/?retryWrites=true&w=majority&appName=SAADdatabase'
    )
    print("Database connected successfully")
except Exception as e:
    print(f"Database connection failed: {e}")
    exit(1)

# Admin database and collections
admin_db = client["SAAD_Admin"]
branch_collection = admin_db["Branch_Collection"]
transaction_collection = admin_db["Transaction_Collection"]
library_collection = admin_db["Library_Collection"]
purchase_order_collection = admin_db["Purchase_Order_Collection"]

# User database and collections
user_db = client["SAAD_User"]
user_collection = user_db["User_Collection"]

# Media database and collections
media_db = client["SAAD_Media"]
media_collection = media_db["Media_Collection"]

# Subscription database and collections
sub_db = client["SAAD_Subscription"]
subscription_collection = sub_db["Subscription_Collection"]