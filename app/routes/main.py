from flask import Blueprint, render_template, Flask, request
import sqlite3
from app.database.database import fetch_all
from app.services.utils import format_number, get_completion_date


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    data = fetch_all()
    agencies = data["agencies"]
    amendment_dates = data["amendment_dates"]
    covid_dates = data["covid_amendment_dates"]

    sort_key = request.args.get("sort", "section_count")
    sort_order = request.args.get("order", "down")

    def get_sort_value(agency):
        value = agency.get(sort_key)
        if value is None: return 0
        else: return value.lower() if isinstance(value, str) else value

    agencies.sort(key=get_sort_value, reverse=(sort_order == "down"))
    for agency in agencies:
        agency["children"].sort(key=get_sort_value, reverse=(sort_order == "down"))

    total_word_count = sum([agency["word_count"] for agency in agencies])
    finish_date = get_completion_date(total_word_count)
    meta = {
        "section_count": format_number(sum([agency["section_count"] + sum([child["section_count"] for child in agency["children"]]) for agency in agencies])),
        "word_count": format_number(total_word_count),
        "covid_count": format_number(sum([agency["covid_count"] + sum([child["covid_count"] for child in agency["children"]]) for agency in agencies])),
    }

    for agency in agencies:
        agency["pretty_word_count"] = format_number(agency["word_count"])
        agency["pretty_section_count"] = format_number(agency["section_count"])
        for child in agency["children"]:
            child["pretty_word_count"] = format_number(child["word_count"])
            child["pretty_section_count"] = format_number(child["section_count"])

    sorted_dates = sorted(amendment_dates.items())
    sorted_covid_dates = sorted(covid_dates.items())

    return render_template(
        "index.html",
        agencies=agencies,
        meta=meta,
        amendment_months = [k for k, v in sorted_dates],
        amendment_counts = [v for k, v in sorted_dates],
        covid_months = [k for k, v in sorted_covid_dates],
        covid_counts = [v for k, v in sorted_covid_dates],
        finish_date = finish_date,
        total_words = total_word_count
    )
