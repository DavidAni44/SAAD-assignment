import os
from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


client = MongoClient(
    f'mongodb+srv://{os.getenv("DBUSERNAME")}:{os.getenv("DBPASSWORD")}'
    '@saaddatabase.8f32e.mongodb.net/?retryWrites=true&w=majority&appName=SAADdatabase'
)

admin_db = client["SAAD_Admin"]

branch_collection = admin_db["Branch_Collection"]
transaction_collection = admin_db["Transaction_Collection"]

user_db = client["SAAD_User"]
user_collection = user_db["User Collection"]

media_db = client["SAAD_Media"]
media_collection = user_db["Media_Collection"]

#singleton pattern