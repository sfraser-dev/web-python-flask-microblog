from flask import Flask
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html><body>
    <h1>Hello, world!</h1>
    </body></html>
    """