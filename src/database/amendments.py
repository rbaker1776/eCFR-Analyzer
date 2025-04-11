import sqlite3
from client import fetch_amendments
from database.dbutils import db_connect
from database.amendment import Amendment


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


if __name__ == "__main__":
    create_amendment_table()
    amendment_db_init()
