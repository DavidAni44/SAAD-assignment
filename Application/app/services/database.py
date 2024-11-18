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
user_collection = db["Users Collection"]
media_collection = db["Media Collection"]
branch_collection = db["Branch Collection"]
library_collection = db["Library Collection"]
transaction_collection = db["Transaction Collection"]
subscription_collection = db["Subscription Collection"]
purchase_order_collection = db["Purchase Order Collection"]

#singleton pattern