from flask import Flask, render_template, request
import sqlite3
from database.database import fetch_all


app = Flask(__name__)


@app.route("/")
def index():
    agencies=fetch_all()

    sort_key = request.args.get("sort", "section_count")
    sort_order = request.args.get("order", "down")

    def get_sort_value(agency):
        value = agency.get(sort_key)
        if value is None: return 0
        else: return value.lower() if isinstance(value, str) else value

    agencies.sort(key=get_sort_value, reverse=(sort_order == "down"))
    for agency in agencies:
        agency["children"].sort(key=get_sort_value, reverse=(sort_order == "down"))

    return render_template("index.html", agencies=agencies)


if __name__ == "__main__":
    app.run()
