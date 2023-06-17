from flask import Flask, render_template, request
from dotenv import load_dotenv
import datetime
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint

# Create a flask app factory via "create_app()".
# This creates apps rather than just hard-coding app in the main file ("app.py").
# This prevents issue when working with databases.
def create_app():
    # Our flask app.
    app = Flask(__name__)
    load_dotenv()
    # Main endpoint decorator.
    @app.route("/", methods=["GET", "POST"])
    def home():
        # Connect app to the DB.
        # client = MongoClient(os.getenv("MONGODB_URI"))
        # It's a test MongoDB Atlas account so this is ok.
        client = MongoClient("mongodb+srv://mong-rabbit:NCO02Xj4IsUnBAKt@jack-rabbit.u44ibnh.mongodb.net/")
        app.db = client.microblog
        # Handle POST request.
        # Two submit buttons on the page (submit & delete) so need to distinguish between
        # them, gave both submit buttons the same name but different values.
        if request.method == "POST":
            if request.form.get("BlogButtons") == "submit":
                entry_content = request.form.get("content")
                formatted_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                app.db.entries.insert_one({"content": entry_content, "date": formatted_date})
            
            else: # request.form.get("BlogButtons") != "submit":
                app.db.entries.delete_one({"_id": ObjectId(request.form.get("BlogButtons"))})

        # Retrieve a list of tuples via list comprehension of the DB entries.
        entries_with_date_and_dbID = [
            (entry["content"], entry["date"], entry["_id"]) for entry in app.db.entries.find({})
        ]

        # Sort this list via date in descending order.
        entries_with_date_and_dbID_sorted = sorted(
            entries_with_date_and_dbID, key=lambda tup: tup[1], reverse=True)

        # my_collection = app.db.entries.find().sort("content")
        # for my_doc in my_collection:
        #     pprint.pprint(my_doc)

        # Return to user the jinja templated "home.html". 
        return render_template("home.html", entries = entries_with_date_and_dbID_sorted)

    # App factory return.
    return app
