from model.transactie import Transactie
import logging
from helpers import logging_config
from db import db_transacties

if __name__ == "__main__":  
    transacties = db_transacties.get_all_transactions()
    if len(transacties) == 0:
        print("Geen transacties in database")
    else:
        for t in transacties:
            print(t)
    
