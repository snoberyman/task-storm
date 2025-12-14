import os

class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]  # will raise KeyError if missing
    MONGO_URI = os.environ.get("") or os.environ.get("MONGO_URI")  # Try  first, then MONGO_URI
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
