from flask import Flask, request, jsonify
from app import create_app
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from dotenv import load_dotenv
from datetime import datetime
from flask_cors import CORS 
from app.api.endpoints.users import ping_endpoint

app = create_app()
CORS(app, resources={r"/*": {
        "origins": ["http://10.75.197.143:5000"],  # Allow this origin
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }})

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
