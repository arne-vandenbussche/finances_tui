import logging
from helpers import logging_config
from db import db_transactions
from tui import transactions_cli

if __name__ == "__main__":  
    while True:
        transactions_cli.menu()
