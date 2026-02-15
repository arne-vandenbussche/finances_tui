from dataclasses import dataclass, field
from datetime import date
import logging


@dataclass
class Transaction:
    id: int = 0
    date_of_transaction: date = field(default_factory=date.today)
    amount: float = 0.0
    payment_method: int | None = None
    partner: int = 0
    in_out: str = "out"
    description: str = ""
    invoice_number: str = ""
    invoice_date: date | None = None
    category: int = 0
    activity: int | None = None
    season: int | None = None
    actuele_rekeningstand: float = 0.0

    def __post_init__(self) -> None:
        if self.in_out not in ("in", "out"):
            logging.getLogger(__name__).warning(
                "Invalid in_out '%s' for Transaction id=%s. Falling back to 'out'.",
                self.in_out,
                self.id,
            )
            self.in_out = "out"

    def __str__(self) -> str:
        return (
            f"Date: {self.date_of_transaction}. "
            f"Amount: {self.amount}. "
            f"Description: {self.description}"
        )
