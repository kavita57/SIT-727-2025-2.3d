from flask import Flask
from config import Config
from extensions import mongo
from journal.routes import journal_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)

    # Ensure the database and collection exist by inserting a dummy document
    with app.app_context():
        
        if mongo.db is None:
            raise RuntimeError("Failed to connect to the MongoDB instance. Please check your MONGO_URI configuration.")
        
        # Check if the database and collection exist, and create them if not
        if mongo.db.entries.count_documents({}) == 0:  # If the collection is empty
            print("Creating initial collection and dummy data...")
            # Insert a dummy entry to create the collection if it doesn't exist
            mongo.db.entries.insert_one({
                "title": "Welcome Entry",
                "content": "This is a dummy entry to ensure the collection is created.",
                "sentiment": "Neutral"
            })

    app.register_blueprint(journal_bp, url_prefix="/")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
