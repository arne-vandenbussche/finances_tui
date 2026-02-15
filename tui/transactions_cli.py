from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Button, DataTable, Footer, Header, Input, Label, Select, Static

from db import db_transactions
from model.transaction import Transaction


def _is_valid_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except (TypeError, ValueError):
        return False


class TransactionsApp(App):
    TITLE = "Finance Transactions"
    SUB_TITLE = "Overview and edit/add"

    CSS = """
    Screen {
        layout: vertical;
    }

    #main {
        height: 1fr;
    }

    #transactions_table {
        width: 2fr;
        height: 1fr;
    }

    #form_panel {
        width: 1fr;
        height: 1fr;
        padding: 0 1;
        border: round $accent;
    }

    .form_label {
        margin-top: 1;
    }

    .form_input {
        margin-bottom: 0;
    }

    #status {
        height: 1;
        margin-top: 1;
        color: $text-muted;
    }

    #actions {
        margin-top: 1;
        height: 3;
    }

    Button {
        margin-right: 1;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self.current_transaction_id: int = 0
        self.lookup_payment_methods: dict[int, str] = {}
        self.lookup_categories: dict[int, str] = {}
        self.lookup_activities: dict[int, str] = {}
        self.lookup_seasons: dict[int, str] = {}
        self.lookup_partners: dict[int, str] = {}

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main"):
            yield DataTable(id="transactions_table", zebra_stripes=True, cursor_type="row")
            with Vertical(id="form_panel"):
                yield Label("Transaction date (YYYY-MM-DD)", classes="form_label")
                yield Input(value=date.today().isoformat(), id="date_input", classes="form_input")

                yield Label("Amount (always positive)", classes="form_label")
                yield Input(value="0", id="amount_input", classes="form_input")

                yield Label("Type", classes="form_label")
                yield Select(options=[("in", "in"), ("out", "out")], id="in_out_select")

                yield Label("Payment method", classes="form_label")
                yield Select(options=[], id="payment_method_select")

                yield Label("Partner", classes="form_label")
                yield Select(options=[], id="partner_select")

                yield Label("Category", classes="form_label")
                yield Select(options=[], id="category_select")

                yield Label("Activity", classes="form_label")
                yield Select(options=[], id="activity_select")

                yield Label("Season", classes="form_label")
                yield Select(options=[], id="season_select")

                yield Label("Invoice number", classes="form_label")
                yield Input(value="", id="invoice_number_input", classes="form_input")

                yield Label("Invoice date (YYYY-MM-DD, optional)", classes="form_label")
                yield Input(value="", id="invoice_date_input", classes="form_input")

                yield Label("Balance (optional)", classes="form_label")
                yield Input(value="", id="balance_input", classes="form_input")

                yield Label("Description", classes="form_label")
                yield Input(value="", id="description_input", classes="form_input")

                with Horizontal(id="actions"):
                    yield Button("New", id="new_button", variant="default")
                    yield Button("Save", id="save_button", variant="success")
                    yield Button("Refresh", id="refresh_button", variant="primary")

                yield Static("Ready", id="status")
        yield Footer()

    def on_mount(self) -> None:
        self._load_lookups()
        self._setup_table()
        self._load_transactions()
        self._clear_form_for_new()

    def _set_status(self, message: str) -> None:
        self.query_one("#status", Static).update(message)

    def _fetch_lookup(self, table_name: str) -> dict[int, str]:
        with db_transactions.get_connection() as conn:
            rows = conn.execute(f"SELECT id, name FROM {table_name} ORDER BY name COLLATE NOCASE").fetchall()
        return {int(row[0]): str(row[1]) for row in rows}

    def _load_lookups(self) -> None:
        self.lookup_payment_methods = self._fetch_lookup("payment_methods")
        self.lookup_categories = self._fetch_lookup("categories")
        self.lookup_activities = self._fetch_lookup("activities")
        self.lookup_seasons = self._fetch_lookup("seasons")
        self.lookup_partners = self._fetch_lookup("partners")

        self._set_select_options("#payment_method_select", self.lookup_payment_methods)
        self._set_select_options("#category_select", self.lookup_categories)
        self._set_select_options("#activity_select", self.lookup_activities)
        self._set_select_options("#season_select", self.lookup_seasons)
        self._set_select_options("#partner_select", self.lookup_partners)

    def _set_select_options(self, selector: str, lookup: dict[int, str]) -> None:
        options = [(name, str(item_id)) for item_id, name in lookup.items()]
        self.query_one(selector, Select).set_options(options)

    def _setup_table(self) -> None:
        table = self.query_one("#transactions_table", DataTable)
        table.add_columns(
            "id",
            "date",
            "amount",
            "type",
            "payment",
            "partner",
            "category",
            "activity",
            "season",
            "description",
        )

    def _load_transactions(self) -> None:
        table = self.query_one("#transactions_table", DataTable)
        table.clear()

        with db_transactions.get_connection() as conn:
            rows = conn.execute(
                """
                SELECT
                    t.id,
                    t.date_of_transaction,
                    t.amount,
                    t.in_out,
                    COALESCE(pm.name, ''),
                    COALESCE(p.name, ''),
                    COALESCE(c.name, ''),
                    COALESCE(a.name, ''),
                    COALESCE(s.name, ''),
                    COALESCE(t.description, '')
                FROM transactions t
                LEFT JOIN payment_methods pm ON pm.id = t.payment_method
                LEFT JOIN partners p ON p.id = t.partner
                LEFT JOIN categories c ON c.id = t.category
                LEFT JOIN activities a ON a.id = t.activity
                LEFT JOIN seasons s ON s.id = t.season
                ORDER BY t.date_of_transaction DESC, t.id DESC
                """
            ).fetchall()

        for row in rows:
            table.add_row(*[str(value) if value is not None else "" for value in row], key=str(row[0]))

        self._set_status(f"Loaded {len(rows)} transactions")

    def _clear_form_for_new(self) -> None:
        self.current_transaction_id = 0
        self.query_one("#date_input", Input).value = date.today().isoformat()
        self.query_one("#amount_input", Input).value = "0"
        self.query_one("#in_out_select", Select).value = "out"
        self.query_one("#invoice_number_input", Input).value = ""
        self.query_one("#invoice_date_input", Input).value = ""
        self.query_one("#balance_input", Input).value = ""
        self.query_one("#description_input", Input).value = ""

        self._set_default_lookup_values()
        self._set_status("New transaction mode")

    def _set_default_lookup_values(self) -> None:
        self._set_default_select_value("#payment_method_select", self.lookup_payment_methods)
        self._set_default_select_value("#partner_select", self.lookup_partners)
        self._set_default_select_value("#category_select", self.lookup_categories)
        self._set_default_select_value("#activity_select", self.lookup_activities)
        self._set_default_select_value("#season_select", self.lookup_seasons)

    def _set_default_select_value(self, selector: str, lookup: dict[int, str]) -> None:
        select = self.query_one(selector, Select)
        unknown_id = None
        for item_id, name in lookup.items():
            if name.strip().lower() == "onbekend":
                unknown_id = item_id
                break
        if unknown_id is not None:
            select.value = str(unknown_id)
        elif lookup:
            first_id = next(iter(lookup.keys()))
            select.value = str(first_id)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        row_key = event.row_key.value
        if row_key is None:
            return

        transaction = db_transactions.get_transaction_by_id(int(row_key))
        if transaction is None:
            self._set_status(f"Transaction {row_key} not found")
            return

        self.current_transaction_id = transaction.id
        self.query_one("#date_input", Input).value = transaction.date_of_transaction.isoformat()
        self.query_one("#amount_input", Input).value = str(transaction.amount)
        self.query_one("#in_out_select", Select).value = transaction.in_out
        self.query_one("#invoice_number_input", Input).value = transaction.invoice_number or ""
        self.query_one("#invoice_date_input", Input).value = (
            transaction.invoice_date.isoformat() if transaction.invoice_date else ""
        )
        self.query_one("#balance_input", Input).value = (
            "" if transaction.actuele_rekeningstand is None else str(transaction.actuele_rekeningstand)
        )
        self.query_one("#description_input", Input).value = transaction.description or ""

        self._set_select_value("#payment_method_select", transaction.payment_method)
        self._set_select_value("#partner_select", transaction.partner)
        self._set_select_value("#category_select", transaction.category)
        self._set_select_value("#activity_select", transaction.activity)
        self._set_select_value("#season_select", transaction.season)

        self._set_status(f"Editing transaction #{transaction.id}")

    def _set_select_value(self, selector: str, value: int | None) -> None:
        select = self.query_one(selector, Select)
        if value is None:
            return
        select.value = str(value)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "new_button":
            self._clear_form_for_new()
            return
        if event.button.id == "refresh_button":
            self._load_lookups()
            self._load_transactions()
            return
        if event.button.id == "save_button":
            self._save_current_form()

    def _parse_required_decimal(self, raw: str, field_name: str) -> Decimal | None:
        try:
            value = Decimal(raw.strip())
            if value < 0:
                value = abs(value)
            return value
        except (InvalidOperation, AttributeError):
            self._set_status(f"Invalid {field_name}: {raw!r}")
            return None

    def _parse_optional_decimal(self, raw: str) -> float | None:
        raw = raw.strip()
        if not raw:
            return None
        try:
            return float(Decimal(raw))
        except (InvalidOperation, ValueError):
            return None

    def _parse_optional_date(self, raw: str) -> date | None:
        raw = raw.strip()
        if not raw:
            return None
        if not _is_valid_date(raw):
            return None
        return datetime.strptime(raw, "%Y-%m-%d").date()

    def _save_current_form(self) -> None:
        date_raw = self.query_one("#date_input", Input).value.strip()
        amount_raw = self.query_one("#amount_input", Input).value.strip()
        invoice_date_raw = self.query_one("#invoice_date_input", Input).value.strip()

        if not _is_valid_date(date_raw):
            self._set_status("date_of_transaction must be YYYY-MM-DD")
            return

        amount_dec = self._parse_required_decimal(amount_raw, "amount")
        if amount_dec is None:
            return

        if invoice_date_raw and not _is_valid_date(invoice_date_raw):
            self._set_status("invoice_date must be YYYY-MM-DD or empty")
            return

        payment_method_value = self.query_one("#payment_method_select", Select).value
        partner_value = self.query_one("#partner_select", Select).value
        category_value = self.query_one("#category_select", Select).value
        activity_value = self.query_one("#activity_select", Select).value
        season_value = self.query_one("#season_select", Select).value

        transaction = Transaction(
            id=self.current_transaction_id,
            date_of_transaction=datetime.strptime(date_raw, "%Y-%m-%d").date(),
            amount=float(amount_dec),
            payment_method=int(payment_method_value) if payment_method_value else None,
            partner=int(partner_value) if partner_value else 0,
            in_out=str(self.query_one("#in_out_select", Select).value or "out"),
            description=self.query_one("#description_input", Input).value.strip(),
            invoice_number=self.query_one("#invoice_number_input", Input).value.strip(),
            invoice_date=self._parse_optional_date(invoice_date_raw),
            category=int(category_value) if category_value else 0,
            activity=int(activity_value) if activity_value else None,
            season=int(season_value) if season_value else None,
            actuele_rekeningstand=self._parse_optional_decimal(
                self.query_one("#balance_input", Input).value
            ),
        )

        db_transactions.save_transaction(transaction)

        self._load_transactions()
        if self.current_transaction_id == 0:
            self._set_status("New transaction saved")
            self._clear_form_for_new()
        else:
            self._set_status(f"Transaction #{self.current_transaction_id} updated")


def run() -> None:
    TransactionsApp().run()
