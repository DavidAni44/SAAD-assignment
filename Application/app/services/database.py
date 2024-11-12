import os
from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


client = MongoClient(
    f'mongodb+srv://{os.getenv("DBUSERNAME")}:{os.getenv("DBPASSWORD")}'
    '@saaddatabase.8f32e.mongodb.net/?retryWrites=true&w=majority&appName=SAADdatabase'
)
db = client["AMLdb"]
user_collection = db["User Data"]
media_collection = db["Media Data"]