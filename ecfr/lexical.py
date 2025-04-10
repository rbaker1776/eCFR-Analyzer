import xml.etree.ElementTree as ET
from client import *


def count_words(s: str) -> int:
    # perhaps will implement more sophisticated algo later
    # this will suffice for now
    return len(s.split())

if __name__ == "__main__":
    agencies = fetch_agencies()
    for agency in agencies:
        print(agency, count_words(text_from_agency(agency)))
