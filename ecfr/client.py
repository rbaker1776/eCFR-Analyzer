import requests
import json
from datetime import datetime
from agency import Agency


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

def versioner_full(date: datetime, title: int) -> str:
    response = requests.get(versioner_full_url(date, title))
    response.raise_for_status()
    print(response.text)


if __name__ == "__main__":
    agencies = fetch_agencies()
    print(count_agencies(agencies))
