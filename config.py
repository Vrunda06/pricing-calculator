import os

class Config:
    SECRET_KEY = os.urandom(24)  # Used for session or JWT encoding/decoding
    SQLALCHEMY_DATABASE_URI = 'sqlite:///pricing_calculator.db'  # SQLite DB file
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.urandom(24)  # JWT secret for encoding
 
