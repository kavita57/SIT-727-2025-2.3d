import os

class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "default_secret_key")
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://dkavita2121:Slappy132@cluster0.dwumgci.mongodb.net/journalDB?retryWrites=true&w=majority&appName=Cluster0")  # Default to local DB