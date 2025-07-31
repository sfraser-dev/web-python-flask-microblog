from flask import Flask, render_template, request, flash
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_wtf import CSRFProtect


# Create a flask app factory via "create_app()". This creates apps rather than just hard-coding app in the main file ("app.py").
# This prevents possible issue when deploying, sometimes this file will get run multiple times when deploying, but the deploying mechanism will be smart enough to only create one app (thanks to the flask app factory).
def create_app():
    # Our flask app.
    app = Flask(__name__)
    # Load env vars.
    load_dotenv()
    # CSRF protection.
    app.secret_key = os.getenv("SECRET_KEY", "insecure-default-key")  # Use env var in production
    CSRFProtect(app)
    # Connect app to the DB.
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client[os.getenv("DB_NAME")]
    # Main endpoint decorator.
    @app.route("/", methods=["GET", "POST"])
    def home():
        db = app.db
        # Handle POST request.
        # Two submit buttons on the page (submit & delete) so need to distinguish between
        # them, gave both submit buttons the same name but different values.
        if request.method == "POST":
            if request.form.get("BlogButtons") == "submit":
                # Sanitise entries, no empty or white space only posts.
                entry_content = request.form.get("content", "").strip()
                # Server side enforcing of max message length.
                if 0 < len(entry_content) <= 140:
                    formatted_date = (datetime.now(timezone.utc)+timedelta(minutes=60)).strftime("%Y-%m-%d %H:%M:%S")
                    db.entries.insert_one({"content": entry_content, "date": formatted_date})
                else:
                    # Flash message that post must be: 1 <= chars <= 140.
                    flash("Post must be between 1 and 140 characters.")
            else: # request.form.get("BlogButtons") != "submit":
                db.entries.delete_one({"_id": ObjectId(request.form.get("BlogButtons"))})

        # Retrieve a list of tuples via list comprehension of the DB entries.
        entries_with_date_and_dbID = [
            (entry["content"], entry["date"], entry["_id"]) for entry in db.entries.find({})
        ]

        # Sort this list via date in descending order.
        entries_with_date_and_dbID_sorted = sorted(
            entries_with_date_and_dbID, key=lambda tup: tup[1], reverse=True)

        # Return to user the jinja templated "home.html". 
        return render_template("home.html", entries = entries_with_date_and_dbID_sorted)

    # App factory return.
    return app
