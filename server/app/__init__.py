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
            # Railway's internal MongoDB URL might not include a database name
            # Ensure the connection string has a database name
            mongo_uri = mongo_uri.rstrip("/")
            
            # Check if database name is already in the URI
            # A proper MongoDB URI format: mongodb://[user:pass@]host[:port][/database]
            # If it ends with just a port number (like :27017), we need to add the database name
            # Split by / and check the last part
            uri_parts = mongo_uri.split("/")
            if len(uri_parts) > 0:
                last_part = uri_parts[-1]
                # If last part contains : (it's host:port) or is empty, add database name
                # Also check if it's just numbers (port) or contains @ (still in auth part)
                if ":" in last_part or "@" in last_part or not last_part or last_part.isdigit():
                    db_name = os.getenv("MONGO_DBNAME", "TaskManager")
                    mongo_uri = mongo_uri + "/" + db_name
                    print(f"Added database name '{db_name}' to MongoDB URI")
                else:
                    print(f"Database name found in URI: {last_part}")
            
            app.config["MONGO_URI"] = mongo_uri
            # Log connection info (hide password)
            if "@" in mongo_uri:
                # Hide password for logging
                parts = mongo_uri.split("@")
                if len(parts) == 2:
                    auth = parts[0].split("://")[-1] if "://" in parts[0] else parts[0]
                    if ":" in auth:
                        user = auth.split(":")[0]
                        safe_uri = mongo_uri.split("://")[0] + "://" + user + ":***@" + parts[1]
                        print(f"MongoDB URI: {safe_uri}")
                    else:
                        print(f"MongoDB URI: {mongo_uri.split('@')[0]}:***@{mongo_uri.split('@')[1]}")
                else:
                    print(f"MongoDB URI configured (credentials hidden)")
            else:
                print(f"MongoDB URI: {mongo_uri}")
        else:
            raise ValueError("DATABASE_URL environment variable is required")
    else:
        print(f"MongoDB URI from config: {app.config.get('MONGO_URI', 'NOT SET')[:50]}...")

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
    
    # Verify MongoDB connection - Flask-PyMongo uses lazy connection
    # So we need to access it within an app context
    def verify_connection():
        try:
            with app.app_context():
                # Force connection by accessing the database
                db = mongo.db
                if db is None:
                    print("ERROR: mongo.db is None after initialization")
                    print(f"MONGO_URI: {app.config.get('MONGO_URI', 'NOT SET')}")
                    return False
                # Try to list collections to verify connection
                collections = db.list_collection_names()
                print(f"MongoDB connected successfully. Database: {db.name}, Collections: {collections}")
                return True
        except Exception as e:
            print(f"ERROR: MongoDB connection failed: {e}")
            print(f"MONGO_URI: {app.config.get('MONGO_URI', 'NOT SET')}")
            import traceback
            traceback.print_exc()
            return False
    
    # Try to verify connection
    verify_connection()

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
