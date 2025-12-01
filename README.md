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


