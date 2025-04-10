import sqlite3
from client import *


def db_connect():
    return sqlite3.connect("app.db")


def clear_ecfr_counts_table():
    conn = db_connect()
    cursor = conn.cursor()
    
    cursor.execute(f"DELETE FROM ecfr_counts")
    
    conn.commit()
    conn.close()

def create_ecfr_counts_table():
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ecfr_counts (
        title TEXT,
        subtitle TEXT,
        chapter TEXT,
        subchapter TEXT,
        part TEXT,
        word_count INTEGER,
        section_count INTEGER,
        covid_count INTEGER,
        UNIQUE(title,subtitle,chapter,subchapter,part)
    );
    """)

    conn.commit()
    conn.close()


def ecfr_insert_data(title, subtitle, chapter, subchapter, part, word_count, section_count, covid_count):
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO ecfr_counts (
        title, subtitle, chapter, subchapter, part, word_count, section_count, covid_count
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (title, subtitle, chapter, subchapter, part, word_count, section_count, covid_count))
    
    conn.commit()
    conn.close()


def ecfr_debug_print(title, subtitle, chapter, subchapter, part):
    print(title, end="->")
    if subtitle is not None: print(subtitle.attrib['N'], end="->")
    if chapter is not None: print(chapter.attrib['N'], end="->")
    if subchapter is not None: print(subchapter.attrib['N'], end="->")
    if part is not None: print(part.attrib['N'], end='\n')

levels = [ None ] * 5

def ecfr_parse_levels():
    title = levels[0]
    subtitle = levels[1].attrib['N'] if levels[1] is not None else ""
    chapter = levels[2].attrib['N'] if levels[2] is not None else ""
    subchapter = levels[3].attrib['N'] if levels[3] is not None else ""
    part = levels[4].attrib['N'] if levels[4] is not None else ""
    return title, subtitle, chapter, subchapter, part

def ecfr_process_elements(parent, tag):
    if tag > 5:
        # we've reached the max depth needed
        # time to count the words!
        #ecfr_debug_print(*levels)
        title, subtitle, chapter, subchapter, part = ecfr_parse_levels()
        n_words = word_count(parent)
        n_sections = len(parent.findall(f".//DIV8"))
        paragraphs = [("".join(p.itertext()).strip()) for p in parent.findall(".//P")]
        n_covid = len([p for p in paragraphs if any(term in p.lower() for term in ["covid", "covid19", "covid-19"])])
        ecfr_insert_data(title, subtitle, chapter, subchapter, part, n_words, n_sections, n_covid)
        return

    elements = parent.findall(f".//DIV{tag}")
    if elements:
        for element in elements:
            levels[tag-1] = element
            ecfr_process_elements(element, tag + 1)
    else:
        levels[tag-1] = None
        ecfr_process_elements(parent, tag + 1)

def ecfr_init():
    for title in range(1, 51):
        print(f"processing title {title}...")
        try:
            xml = title_xml(title)
            levels[0] = title
            ecfr_process_elements(xml, 2)
        except Exception as e:
            print(e)


def ecfr_build_query(title, subtitle, chapter, subchapter, part):
    query = "SELECT * FROM ecfr_counts WHERE 1=1"
    params = []

    if title is not None:
        query += " AND title = ?"
        params.append(title)
    if subtitle is not None:
        query += " AND subtitle = ?"
        params.append(subtitle)
    if chapter is not None:
        query += " AND chapter = ?"
        params.append(chapter)
    if subchapter is not None:
        query += " AND subchapter = ?"
        params.append(subchapter)
    if part is not None:
        query += " AND part = ?"
        params.append(part)

    return query, params

def ecfr_query(title=None, subtitle=None, chapter=None, subchapter=None, part=None):
    conn = db_connect()
    cursor = conn.cursor()

    query, params = ecfr_build_query(title, subtitle, chapter, subchapter, part)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    n_words = sum([row[5] for row in rows])
    n_sections = sum([row[6] for row in rows])
    n_covid_paragraphs = sum([row[7] for row in rows])
    return {
        "n_words": n_words,
        "n_sections": n_sections,
        "n_covid_paragraphs": n_covid_paragraphs,
    }


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

def agency_insert_data(name, short_name, display_name, sortable_name, slug, children, cfr_references):
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO agencies (
        name, short_name, display_name, sortable_name, slug, children, cfr_references
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, short_name, display_name, sortable_name, slug, children, cfr_references))
    
    conn.commit()
    conn.close()

def agency_init():
    agencies = fetch_agencies()
    for a in agencies:
        agency_insert_data(a.name, a.short_name, a.display_name, a.sortable_name, a.slug, str(a.children), str(a.cfr_references))


def agency_query(name=None, short_name=None, sortable_name=None):
    query = "SELECT * FROM agencies WHERE 1=1"
    params = []

    if name is not None:
        query += " AND name = ?"
        params.append(name)
    if short_name is not None:
        query += " AND short_name = ?"
        params.append(short_name)
    if sortable_name is not None:
        query += " AND sortable_name = ?"
        params.append(sortable_name)

    return query, params

def agency_query(name=None, short_name=None, sortable_name=None):
    conn = db_connect()
    cursor = conn.cursor()

    query, params = agency_query(name, short_name, sortable_name)
    cursor.execute(query, params)
    agency = cursor.fetchall()[0]

    return {
        "children": agency[6],
    }


if __name__ == "__main__":
    create_ecfr_counts_table()
    create_agency_table()
    agency_init()
    #ecfr_init()
