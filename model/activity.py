from dataclasses import dataclass


@dataclass
class Activity:
    id: int = 0
    name: str = ""
    description: str = ""
