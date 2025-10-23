from model.transactie import Transactie
import logging
from helpers import logging_config
from db import db_transacties
from tui import crud

if __name__ == "__main__":  
    while True:
        crud.menu()
