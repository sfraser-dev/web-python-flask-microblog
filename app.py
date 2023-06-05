from flask import Flask, render_template, request
from dotenv import load_dotenv
import datetime
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint

def create_app():
    app = Flask(__name__)
    load_dotenv()
    @app.route("/", methods=["GET", "POST"])
    def home():
        client = MongoClient(os.getenv("MONGODB_URI"))
        app.db = client.microblog
        if request.method == "POST":
            if request.form.get("BlogButtons") == "submit":
                entry_content = request.form.get("content")
                formatted_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                app.db.entries.insert_one({"content": entry_content, "date": formatted_date})
            
            else: # request.form.get("BlogButtons") != "submit":
                app.db.entries.delete_one({"_id": ObjectId(request.form.get("BlogButtons"))})

        entries_with_date_and_dbID = [
            (entry["content"], entry["date"], entry["_id"]) for entry in app.db.entries.find({})
        ]
        entries_with_date_and_dbID_sorted = sorted(
            entries_with_date_and_dbID, key=lambda tup: tup[1], reverse=True)

        # my_collection = app.db.entries.find().sort("content")
        # for my_doc in my_collection:
        #     pprint.pprint(my_doc)

        return render_template("home.html", entries = entries_with_date_and_dbID_sorted)

    return app