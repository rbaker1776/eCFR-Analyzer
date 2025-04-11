import sqlite3
from client import title_xml, word_count
from database.dbutils import db_connect
from database.page import Page


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

def ecfr_insert_data(page: Page, word_count: int, section_count: int, covid_count: int):
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO ecfr_counts (
        title, subtitle, chapter, subchapter, part, word_count, section_count, covid_count
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (page.title, page.subtitle, page.chapter, page.subchapter, page.part, word_count, section_count, covid_count))
    
    conn.commit()
    conn.close()


current_page = Page()

def ecfr_process_elements(parent, tag):
    if tag > 5:
        # we've reached the max depth needed, time to count the words!
        #print(current_page)
        n_words = word_count(parent)
        n_sections = len(parent.findall(f".//DIV8"))

        paragraphs = [("".join(p.itertext()).strip()) for p in parent.findall(".//P")]
        n_covid = len([p for p in paragraphs if any(term in p.lower() for term in ["covid", "covid19", "covid-19"])])

        ecfr_insert_data(current_page, n_words, n_sections, n_covid)

    else:
        elements = parent.findall(f".//DIV{tag}")
        if elements:
            for element in elements:
                if tag == 2: current_page.subtitle = element.attrib['N']
                elif tag == 3: current_page.chapter = element.attrib['N']
                elif tag == 4: current_page.subchapter = element.attrib['N']
                elif tag == 5: current_page.part = element.attrib['N']
                ecfr_process_elements(element, tag + 1)
        else:
            if tag == 2: current_page.subtitle = ""
            elif tag == 3: current_page.chapter = parent.attrib['N']
            elif tag == 4: current_page.subchapter = parent.attrib['N']
            elif tag == 5: current_page.part = parent.attrib['N']
            ecfr_process_elements(parent, tag + 1)


def ecfr_db_init():
    for title in range(35, 40):
        print(f"(ecfr_db_init): processing title {title}...")
        if title == 35: # title 35 is reserved
            continue
        #try:
        xml = title_xml(title)
        current_page.title = title 
        ecfr_process_elements(xml, 2)
        #except Exception as e:
        #    print(e)


def ecfr_build_query(page: Page):
    query = "SELECT * FROM ecfr_counts WHERE 1=1"
    params = []

    if page.title != "":
        query += " AND title = ?"
        params.append(page.title)
    if page.subtitle != "":
        query += " AND subtitle = ?"
        params.append(page.subtitle)
    if page.chapter != "":
        query += " AND chapter = ?"
        params.append(page.chapter)
    if page.subchapter != "":
        query += " AND subchapter = ?"
        params.append(page.subchapter)
    if page.part != "":
        query += " AND part = ?"
        params.append(page.part)

    return query, params

def ecfr_query(page: Page):
    conn = db_connect()
    cursor = conn.cursor()

    query, params = ecfr_build_query(page)
    cursor.execute(query, params)
    rows = cursor.fetchall()

    n_words = sum([row[5] for row in rows])
    n_sections = sum([row[6] for row in rows])
    n_covid_paragraphs = sum([row[7] for row in rows])

    conn.commit()
    conn.close()

    return {
        "word_count": n_words,
        "section_count": n_sections,
        "covid_count": n_covid_paragraphs,
    }


if __name__ == "__main__":
    ecfr_db_init()
