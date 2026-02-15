from dataclasses import dataclass


@dataclass
class Partner:
    id: int = 0
    name: str = ""
    bank_account: str = ""
    description: str = ""
