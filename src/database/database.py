import sqlite3
from database.dbutils import db_connect
from database.ecfr_counts import ecfr_query, ecfr_db_init
from database.agencies import agency_query, agency_db_init
from database.amendments import amendment_query, amendment_db_init 
from database.page import Page
from collections import Counter
import math


def fetch_agencies() -> dict:
    agencies = agency_query()
    for i, agency in enumerate(agencies):
        agency["word_count"] = 0
        agency["section_count"] = 0
        agency["covid_count"] = 0
        agency["child_count"] = len(agency["children"])

        for reference in agency["cfr_references"]:
            stats = ecfr_query(Page.from_json(reference))
            for field in ["word_count", "section_count", "covid_count"]:
                agency[field] += stats[field]

    # unflatten our list
    for i in range(len(agencies)):
        if (i >= len(agencies)):
            break
        agencies[i]["children"] = []
        for j in range(agencies[i]["child_count"]):
            agencies[i]["children"].append(agencies.pop(i + 1))
            agencies[i]["children"][-1]["name"] = agencies[i]["children"][-1]["name"].split(',')[0]

    for agency in agencies:
        agency["abbrev"] = agency["abbrev"] or ""
        for child in agency["children"]:
            for field in ["word_count", "section_count", "covid_count"]:
                agency[field] += child[field]

    return agencies


def fetch_amendment_dates() -> dict:
    amendments = amendment_query()
    dates = [amendment["amendment_date"] for amendment in amendments]
    print(len(dates))
    months = [f"{i:4}-{j:02}" for i in range(2003, 2026) for j in range(1, 13)]
    counts = Counter(date[:7] for date in dates)
    for month in months:
        if month not in counts:
            counts[month] = 0
    counts = { k: v for k, v in counts.items() if k >= "2015-01-01" }
    return counts


def fetch_all() -> dict:
    return {
        "agencies": fetch_agencies(),
        "amendment_dates": fetch_amendment_dates(),
    }


if __name__ == "__main__":
    fetch_all()
    pass
