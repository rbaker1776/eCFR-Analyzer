import requests
import json
from datetime import datetime
from agency import Agency
import xml.etree.ElementTree as ET


BASE_URL = "https://www.ecfr.gov"


def fetch_agencies() -> list:
    response = requests.get(f"{BASE_URL}/api/admin/v1/agencies.json")
    response.raise_for_status()
    # response.json() returns a dict with a single key: "agencies"
    agencies = [Agency.from_json(a) for a in response.json()["agencies"]]
    return agencies

def count_agencies(agencies: list) -> int:
    n = 0
    for a in agencies:
        n += 1 + count_agencies(a.children)
    return n


def versioner_structure_url(date: datetime, title: int) -> str:
    return f"{BASE_URL}/api/versioner/v1/structure/{date.strftime('%Y-%m-%d')}/title-{title}.json"

def versioner_structure(date: datetime, title: int) -> dict:
    response = requests.get(versioner_structure_url(date, title))
    response.raise_for_status()
    return response.json()


def versioner_full_url(date: datetime, title: int) -> str:
    return f"{BASE_URL}/api/versioner/v1/full/{date.strftime('%Y-%m-%d')}/title-{title}.xml"

def versioner_full(date: datetime, title: int) -> ET.Element:
    response = requests.get(versioner_full_url(date, title))
    response.raise_for_status()
    return ET.fromstring(response.content)

def text_in_chapter(root: ET.Element, chapter: str) -> str:
    chapter = root.find(f".//DIV3[@N='{chapter}']")
    paragraphs = chapter.findall(".//P")
    paragraphs = [("".join(p.itertext()).strip()) for p in paragraphs]
    text = '\n'.join(paragraphs)
    return text

def text_from_agency(agency: Agency) -> str:
    chapter_texts = [text_in_chapter(versioner_full(datetime(2025, 1, 20), ref["title"]), ref["chapter"]) for ref in agency.cfr_references]
    return '\n'.join(chapter_texts)


if __name__ == "__main__":
    pass
