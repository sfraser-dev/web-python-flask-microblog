from flask import Flask, render_template, request
from dotenv import load_dotenv
import datetime
import os
from pymongo import MongoClient

def create_app():
    load_dotenv()
    app = Flask(__name__)
    @app.route("/", methods=["GET", "POST"])
    def home():
        client = MongoClient(os.getenv("MONGODB_URI"))
        app.db = client.microblog
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})
        
        entries_with_date = [(entry["content"], entry["date"]) for entry in app.db.entries.find({})]
        sorted_by_date = sorted(entries_with_date, key=lambda tup: tup[1], reverse=True)
        return render_template("home.html", entries = sorted_by_date)
    return app