# Purpose

A small TUI application to manage financial transactions of a club.

# Technology

- Python (from 3.11)

# Libraries
(see requirements.txt)

- environs: to read settings from .env file.

# Functions

- Show all transactions

# Planned functions

- Add a transaction
- Update a transactions
- Remove a transaction
- Export to csv
- Filter options when viewing the transactions

# Database name

Create a file `.env` in the main folder. Add the text: 

```text
DATABASE=name_of_database
```

Replace the name of the database by the name you want to use. If the database does not exist, it will be created.

# How to execute

1. Clone the repository or download the code.

2. Create a virtual environment.

```bash
python -m venv .venv
```

3. Install external libraries

```bash
pip install -r requirements.txt
```

4. Execute the code

```
python -m main
```

# Structure of the database

The database consists of these tables:

```sql
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    date_of_transaction TEXT NOT NULL,
    bedrag REAL NOT NULL DEFAULT 0,
    payment_method INTEGER REFERENCES payment_methods(id),
    partner INTEGER NOT NULL REFERENCES partners(id),
    in_out TEXT CHECK (in_out IN ('in', 'out')) NOT NULL,
    description TEXT,
    invoice_number TEXT,
    invoice_date DATE,
    category INTEGER NOT NULL REFERENCES categories(id),
    activity INTEGER REFERENCES activities(id),
    season INTEGER REFERENCES seasons(id),
    actuele_rekeningstand REAL
);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS activities (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS partners (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    bank_account TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS payment_methods (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS seasons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);
```
