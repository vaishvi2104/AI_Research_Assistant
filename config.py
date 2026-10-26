import os

class Config:
    SECRET_KEY = "your-secret-key-change-this-later"

    SQLALCHEMY_DATABASE_URI = "sqlite:///research_assistant.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

    MAX_CONTENT_LENGTH = 20 * 1024 * 1024