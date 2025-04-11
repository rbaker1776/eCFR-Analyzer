import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from database.agency import Agency


BASE_URL = "https://www.ecfr.gov"

date = datetime(2025, 1, 20)


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


def versioner_structure_url(title: int) -> str:
    return f"{BASE_URL}/api/versioner/v1/structure/{date.strftime('%Y-%m-%d')}/title-{title}.json"

def title_structure(title: int) -> dict:
    timeout: int = 5 # seconds
    try:
        response = requests.get(versioner_structure_url(title), timeout=timeout)
        j = response.json()
        return j
    except requests.exceptions.Timeout:
        print(f"Request for title {title} structure timed out after {timeout} seconds")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred fetching title {title} structure: {e}")

def title_chapters(title: int) -> list[str]:
    children = title_structure(title)["children"]
    chapters = [child["identifier"] for child in children]
    return chapters

def versioner_full_url(title: int) -> str:
    return f"{BASE_URL}/api/versioner/v1/full/{date.strftime('%Y-%m-%d')}/title-{title}.xml"

def title_xml(title: int) -> ET.Element:
    timeout: int = 60 * 60 # seconds
    response = requests.get(f"https://www.govinfo.gov/bulkdata/ECFR/title-{title}/ECFR-title{title}.xml", timeout=timeout, stream=True)
    xml_content = b""
    for chunk in response.iter_content(chunk_size=1024 * 1024):
        if chunk:
            xml_content += chunk
    s = ET.fromstring(xml_content)
    return s

def word_count(xml: ET.Element) -> int:
    paragraphs = xml.findall(".//P")
    paragraphs = [("".join(p.itertext()).strip()) for p in paragraphs]
    text = '\n'.join(paragraphs)
    return len(text.split())


if __name__ == "__main__":
    print(title_chapters(2)[0])
#    print([s.attrib["TYPE"] for s in title_xml(2).findall(f".//DIV2")])
