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

    # Register blueprints
    app.register_blueprint(tasks_bp, url_prefix="/graphql")

    @app.before_request
    def before_any_request():
        print("Before request:", request.path)

    @app.after_request
    def after_any_request(response):
        print("After request:", request.path)
        return response

    return app
