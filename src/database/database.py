import sqlite3
from database.dbutils import db_connect
from database.ecfr_counts import ecfr_query, ecfr_db_init
from database.agencies import agency_query, agency_db_init
from database.page import Page


def fetch_all() -> dict:
    agencies = agency_query()
    for i, agency in enumerate(agencies):
        agency["word_count"] = 0
        agency["section_count"] = 0
        agency["covid_count"] = 0
        agency["child_count"] = len(agency["children"])

        for reference in agency["cfr_references"]:
            if agency["abbrev"] == "EPA":
                print(reference)
                print(ecfr_query(Page.from_json(reference)))
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
        for child in agency["children"]:
            for field in ["word_count", "section_count", "covid_count"]:
                agency[field] += child[field]

    return agencies


if __name__ == "__main__":
    #ecfr_db_init()
    #agency_db_init()
    fetch_all()
    pass
