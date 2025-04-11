from typing import List, Dict, Optional


class Agency:
    def __init__(self, name: str, short_name: str, display_name: str, sortable_name: str, slug: str, children: Optional[List["Agency"]] = None, cfr_references: Optional[List[Dict[str, str]]] = None):
        self.name = name
        self.short_name = short_name
        self.display_name = display_name
        self.sortable_name = sortable_name
        self.slug = slug
        self.children = children or []
        self.cfr_references = cfr_references or []

    # constructor to work seamlessly with JSON returned by API
    @classmethod
    def from_json(cls, data: dict) -> "Agency":
        children = [cls.from_json(child) for child in data.get("children", [])]
        return cls(
            name = data.get("name", ""),
            short_name = data.get("short_name", ""),
            display_name = data.get("display_name", ""),
            sortable_name = data.get("sortable_name", ""),
            slug = data.get("slug", ""),
            children = children,
            cfr_references = data.get("cfr_references", [])
        )

    def __repr__(self):
        return f"<Agency: {self.display_name or self.name}>"
