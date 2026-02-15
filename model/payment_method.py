from dataclasses import dataclass


@dataclass
class PaymentMethod:
    id: int = 0
    name: str = ""
    description: str = ""
