import os

class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]  # will raise KeyError if missing
    MONGO_URI = os.environ["DATABASE_URL"]  # no default, must exist
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
