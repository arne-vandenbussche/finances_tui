from model.transactie import Transactie
import db.db_transacties
import sys

def toon_alle_transacties():
    transacties = []
    transacties = db.db_transacties.get_all_transactions()
    if len(transacties) == 0:
        print("There aren't any transactions in this database.")
    for transactie in transacties:
        print(transactie)

def voeg_een_transactie_toe():
    print("Our apologies. We haven't implemented this function yet.")

def exporteer_de_transacties_naar_csv():
    print("Our apologies. The function to export to csv has not been implemented yet.")

def programma_verlaten():
    sys.exit(0)


def menu():
    print(
"""
1. Show all transactions.
2. Add a transaction.
3. Export all transactions to a csv file.
4. Leave the application.
""")
    keuze_succesvol = False
    while not keuze_succesvol:
        try:
            keuze = int(input("Enter the number of your choice: "))
            print(f"This was your choice: {keuze}")
            if keuze in (1, 2, 3, 4):
                keuze_succesvol = True
            else:
                print("You have to give a number from 1 to 4.")
        except ValueError:
            print("You must enter a whole number from 1 to 4.")
    if keuze == 1:
        toon_alle_transacties()
    elif keuze == 2:
        voeg_een_transactie_toe()
    elif keuze == 3:
        exporteer_de_transacties_naar_csv()
    else:
        programma_verlaten()
