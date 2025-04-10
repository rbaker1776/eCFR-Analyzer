from typing import List, Dict, Optional


class Page:
    def __init__(self, title: str="", subtitle: str="", chapter: str="", subchapter: str="", part: str=""):
        self.title = title
        self.subtitle = subtitle
        self.chapter = chapter
        self.subchapter = subchapter
        self.part = part

    @classmethod
    def from_json(cls, data: dict) -> "Page":
        return cls(
            title = data.get("title", ""),
            subtitle = data.get("subtitle", ""),
            chapter = data.get("chapter", ""),
            subchapter = data.get("subchapter", ""),
            part = data.get("part", ""),
        )

    def __repr__(self):
        return f"<Page: {self.title}~{self.subtitle}~{self.chapter}~{self.subchapter}~{self.part}>"
