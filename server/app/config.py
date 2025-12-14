import os

class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]  # will raise KeyError if missing
    MONGO_URI = os.environ.get("DATABASE_URL") or os.environ.get("MONGO_URI")  # Try DATABASE_URL first, then MONGO_URI
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
