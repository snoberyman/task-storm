# app/__init__.py
from flask import Flask, request
from .extensions import mongo
from .graphql.tasks_graphql import tasks_bp
from flask_cors import CORS
import os

def create_app(config_object=None):
    app = Flask(__name__, instance_relative_config=True)

    # Load config
    if config_object:
        app.config.from_object(config_object)
    
    # Ensure MONGO_URI is set (Flask-PyMongo requires this)
    if "MONGO_URI" not in app.config:
        mongo_uri = os.getenv("DATABASE_URL")
        if mongo_uri:
            print(f"Using DATABASE_URL for MONGO_URI: {mongo_uri}")
            # Add database name if not present
            mongo_uri = mongo_uri.rstrip("/")
            if mongo_uri.count("/") <= 2:  # No database name in URI
                db_name = os.getenv("MONGO_DBNAME", "TaskManager")
                mongo_uri = mongo_uri + "/" + db_name
            app.config["MONGO_URI"] = mongo_uri
        else:
            raise ValueError("DATABASE_URL environment variable is required")

    # Allow requests from frontend
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    CORS(
        app,
        origins=[frontend_url],
        supports_credentials=True,
        methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"]
    )

    # Initialize extensions
    mongo.init_app(app)

    # Register blueprints (blueprint already has url_prefix="/graphql", so don't add it again)
    app.register_blueprint(tasks_bp)

    @app.before_request
    def before_any_request():
        print("Before request:", request.path)
        # Ensure MongoDB connection is established
        try:
            if mongo.db is None:
                print("WARNING: mongo.db is None, attempting to reconnect...")
                # Re-initialize if needed
                mongo.init_app(app)
        except Exception as e:
            print(f"WARNING: Error checking MongoDB connection: {e}")

    @app.after_request
    def after_any_request(response):
        print("After request:", request.path)
        return response

    return app
