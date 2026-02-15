from dataclasses import dataclass


@dataclass
class Category:
    id: int = 0
    name: str = ""
    description: str = ""
