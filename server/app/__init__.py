# app/__init__.py
from flask import Flask, app, request
from .extensions import mongo  # or db if using SQLAlchemy
# from app.routes.tasks_graphql import tasks_bp
from .graphql.tasks_graphql import tasks_bp
from flask_cors import CORS
import os

def create_app(config_object=None):
    # Enable instance folder and load instance/config.py
    app = Flask(__name__, instance_relative_config=True)

    # Load config: either from argument, or from instance/config.py
    app.config.from_object(config_object)
    # if config_object:
        
    # else:
    #     app.config.from_pyfile("config.py")  # loads instance/config.py

   # Allow requests from the Vite frontend (adjust origin if needed)
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

    CORS(app, origins=[frontend_url], supports_credentials=True)
    # Initialize extensions
    mongo.init_app(app)  # if using PyMongo

    # app.register_blueprint(tasks_bp)
    app.register_blueprint(tasks_bp)
    
    @app.before_request
    def before_any_request():
        print("Before request:", request.path)

    @app.after_request
    def after_any_request(response):
        print("After request:", request.path)
        return response
    

    return app
