from flask import Blueprint
from .endpoints import media, subscriptions, users

# Define the main API Blueprint without static and template folders
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Register each endpoint Blueprint
api_bp.register_blueprint(users.user_bp)
api_bp.register_blueprint(subscriptions.subscription_bp)
api_bp.register_blueprint(media.media_bp)

def init_api(app):
    app.register_blueprint(api_bp)
