from typing import List, Dict, Optional


class Amendment:
    def __init__(self, date: str="", amendment_date: str="", identifier: str="", name: str="", substantive: bool=True, removed: bool=False, title: str=""):
        self.date = date
        self.amendment_date = amendment_date
        self.identifier = identifier
        self.name = name
        self.substantive = substantive
        self.removed = removed
        self.title = title

    @classmethod
    def from_json(cls, data: dict) -> "Page":
        return cls(
            date = data.get("date", ""),
            amendment_date = data.get("amendment_date", ""),
            identifier = data.get("identifier", ""),
            name = data.get("name", ""),
            substantive = data.get("substantive", ""),
            removed = data.get("removed", ""),
            title = data.get("title", "")
        )

    def __repr__(self):
        return f"<Amendment: {self.title} @ {self.amendment_date}>"
