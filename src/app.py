from flask import Flask, render_template
import sqlite3
from database import fetch_all


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", departments = fetch_all())


if __name__ == "__main__":
    app.run()
