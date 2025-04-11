import sqlite3
from client import fetch_agencies
from database.dbutils import db_connect
from database.agency import Agency
import re


def create_agency_table():
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agencies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        short_name TEXT,
        display_name TEXT,
        sortable_name TEXT,
        slug TEXT,
        children TEXT,
        cfr_references TEXT,
        UNIQUE(sortable_name)
    );
    """)

    conn.commit()
    conn.close()


def agency_insert_data(agency: Agency):
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO agencies (
        name, short_name, display_name, sortable_name, slug, children, cfr_references
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        agency.name,
        agency.short_name,
        agency.display_name,
        agency.sortable_name,
        agency.slug,
        str(agency.children),
        str(agency.cfr_references)
    ))
    
    conn.commit()
    conn.close()


def agency_db_init():
    agencies = fetch_agencies()
    for a in agencies:
        agency_insert_data(a)
        for child in a.children:
            agency_insert_data(child)


def agency_parse_children(children: str):
    children = children.strip("[]")
    children = children.split('>, <')

    agencies = []
    for child in children:
        child = child.strip("<>")
        match = re.match(r"Agency: (.*?), (.*)", child)
        if match:
            name = match.group(1).strip()
            parent = match.group(2).strip()
            agencies.append({
                "name": name,
                "parent": parent,
            })
    return agencies

def build_agency_query(agency: Agency):
    query = "SELECT * FROM agencies WHERE 1=1"
    params = []
    if agency is None:
        return query, params

    if agency.name != "":
        query += " AND name = ?"
        params.append(agency.name)
    if agency.short_name != "":
        query += " AND short_name = ?"
        params.append(agency.short_name)
    if agency.sortable_name != "":
        query += " AND sortable_name = ?"
        params.append(agency.sortable_name)

    return query, params

def agency_query(agency: Agency = None):
    conn = db_connect()
    cursor = conn.cursor()

    query, params = build_agency_query(agency)
    cursor.execute(query, params)
    agencies = cursor.fetchall()

    conn.commit()
    conn.close()

    return [{
        "name": agency[3], # use the display name
        "abbrev": agency[2],
        "children": agency_parse_children(agency[6]),
        "cfr_references": eval(agency[7]),
    } for agency in agencies]


if __name__ == "__main__":
    agency_parse_children("[<Agency: Agricultural Marketing Service, Department of Agriculture>, <Agency: Agricultural Research Service, Department of Agriculture>, <Agency: Animal and Plant Health Inspection Service, Department of Agriculture>, <Agency: Commodity Credit Corporation, Department of Agriculture>, <Agency: Economic Research Service, Department of Agriculture>, <Agency: Farm Service Agency, Department of Agriculture>, <Agency: Federal Crop Insurance Corporation, Department of Agriculture>, <Agency: Food and Nutrition Service, Department of Agriculture>, <Agency: Food Safety and Inspection Service, Department of Agriculture>, <Agency: Foreign Agricultural Service, Department of Agriculture>, <Agency: Forest Service, Department of Agriculture>, <Agency: National Agricultural Statistics Service, Department of Agriculture>, <Agency: National Institute of Food and Agriculture, Department of Agriculture>, <Agency: Natural Resources Conservation Service, Department of Agriculture>, <Agency: Office of Advocacy and Outreach, Department of Agriculture>, <Agency: Office of Chief Financial Officer, Department of Agriculture>, <Agency: Office of Energy Policy and New Uses, Department of Agriculture>, <Agency: Office of Environmental Quality, Department of Agriculture>, <Agency: Office of Information Resources Management, Department of Agriculture>, <Agency: Office of Inspector General, Department of Agriculture>, <Agency: Office of Operations, Department of Agriculture>, <Agency: Office of Procurement and Property Management, Department of Agriculture>, <Agency: Office of Secretary of Agriculture, Department of Agriculture>, <Agency: Office of Transportation, Department of Agriculture>, <Agency: Rural Business-Cooperative Service, Department of Agriculture>, <Agency: Rural Housing Service, Department of Agriculture>, <Agency: Rural Utilities Service, Department of Agriculture>, <Agency: World Agricultural Outlook Board, Department of Agriculture>]")
    pass
