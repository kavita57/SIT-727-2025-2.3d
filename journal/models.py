from extensions import mongo
from textblob import TextBlob

class JournalEntry:
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.sentiment = self.analyze_sentiment()

    def analyze_sentiment(self):
        analysis = TextBlob(self.content)
        if analysis.sentiment.polarity > 0:
            return "Positive"
        elif analysis.sentiment.polarity == 0:
            return "Neutral"
        else:
            return "Negative"

    def save_to_db(self):
        mongo.db.entries.insert_one({
            "title": self.title,
            "content": self.content,
            "sentiment": self.sentiment
        })

    @staticmethod
    def get_all_entries():
        return list(mongo.db.entries.find())
