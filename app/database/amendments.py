import json
import sqlite3
from app.services.client import fetch_amendments, fetch_amendment_meta, count_amendments
from app.database.dbutils import db_connect
from app.models.amendment import Amendment


def create_amendment_table():
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS amendments (
        date TEXT,
        amendment_date TEXT,
        identifier TEXT,
        name TEXT,
        substantive BOOLEAN,
        removed BOOLEAN,
        title TEXT,
        UNIQUE(identifier, name, date, amendment_date, title)
    );
    """)

    conn.commit()
    conn.close()

def amendments_insert_data(amendment: Amendment):
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO amendments (
        date, amendment_date, identifier, name, substantive, removed, title
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (amendment.date, amendment.amendment_date, amendment.identifier, amendment.name, amendment.substantive, amendment.removed, amendment.title))
    
    conn.commit()
    conn.close()
    

def amendment_db_init():
    for title in range(1, 51):
        print(f"(amendment_db_init): processing title {title}...")
        if title == 35: # title 35 is reserved
            continue
        amendments = fetch_amendments(title)
        for amendment in amendments:
            amendments_insert_data(amendment)


def amendment_build_query(amendment: Amendment):
    query = "SELECT * FROM amendments WHERE 1=1"
    params = []

    if amendment is None:
        return query, params

    if amendment.date != "":
        query += " AND date = ?"
        params.append(amendment.date)
    if amendment.amendment_date != "":
        query += " AND amendment_date = ?"
        params.append(amendment.amendment_date)
    if amendment.identifier != "":
        query += " AND identifier = ?"
        params.append(amendment.identifier)
    if amendment.name != "":
        query += " AND name = ?"
        params.append(amendment.name)
    if amendment.substantive != "":
        query += " AND substantive = ?"
        params.append(amendment.substantive)
    if amendment.removed != "":
        query += " AND removed = ?"
        parmas.append(amendment.removed)
    if amendment.title != "":
        query += " AND title = ?"
        params.append(amendment.title)

    return query, params

def amendment_query(amendment: Amendment=None):
    conn = db_connect()
    cursor = conn.cursor()

    query, params = amendment_build_query(amendment)
    cursor.execute(query, params)
    rows = cursor.fetchall()

    conn.commit()
    conn.close()

    return [{
        "date": amendment[0],
        "amendment_date": amendment[1],
        "identifier": amendment[2],
        "name": amendment[3],
        "substantive": amendment[4],
        "removed": amendment[5],
        "title": amendment[6],
    } for amendment in rows]


if __name__ == "__main__":
    #print(amendment_query(Amendment.from_json({})))
    print(count_amendments())
    #create_amendment_table()
    #amendment_db_init()
    pass
