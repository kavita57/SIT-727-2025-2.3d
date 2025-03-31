from flask import Blueprint, render_template, request, redirect, url_for
from journal.models import JournalEntry
from extensions import mongo

journal_bp = Blueprint("journal", __name__)

# Route for displaying all journal entries
@journal_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        sentiment = request.form["sentiment"]
        entry = JournalEntry(title, content,sentiment)
        entry.save_to_db()  # Save entry to MongoDB
        return redirect(url_for("journal.index"))

    entries = JournalEntry.get_all_entries()  # Get all journal entries from DB
    return render_template("home.html", entries=entries)

# Route for creating a new journal entry
@journal_bp.route("/new", methods=["GET", "POST"])
def new_entry():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        entry = JournalEntry(title, content)
        entry.save_to_db()  # Save new entry to MongoDB
        return redirect(url_for("journal.index"))  # Redirect back to the home page with all entries

    return render_template("new_entry.html")  # Render the form page for adding a new entry

# Route for viewing a specific journal entry
@journal_bp.route("/entry/<entry_id>")
def entry(entry_id):
    entry = mongo.db.entries.find_one_or_404({"_id": mongo.db.ObjectId(entry_id)})
    return render_template("entry.html", entry=entry)
