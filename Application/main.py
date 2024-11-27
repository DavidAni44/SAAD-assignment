from flask import Flask, request, jsonify
from app import create_app
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from dotenv import load_dotenv
from datetime import datetime





app = create_app()

from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import requests

app = Flask(__name__)

def ping_endpoint():
    try:
        response = requests.get('http://127.0.0.1:5000/api/users/ping')  # Replace with your actual endpoint
        print(f"Pinged API. Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error pinging API: {e}")

@app.teardown_appcontext
def shutdown_scheduler(exception=None):
    try:
        if scheduler.running:
            scheduler.shutdown()
    except Exception as e:
        print(f"Error shutting down scheduler: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(func=ping_endpoint, trigger="interval", minutes=1)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
