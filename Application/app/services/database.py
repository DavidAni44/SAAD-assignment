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
user_collection = db["Test Users Collection"]
media_collection = db["Test Media Collection"]
branch_collection = db["Test Branch Collection"]
library_collection = db["Library Collection"]
transaction_collection = db["Test Transaction Collection"]
subscription_collection = db["Subscription Collection"]
purchase_order_collection = db["Purchase Order Collection"]

#singleton pattern