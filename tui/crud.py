from model.transactie import Transactie
import db.db_transacties
import services
import sys

def toon_alle_transacties():
    transacties = db.db_transacties.get_all_transactions()
    for transactie in transacties:
        print(transactie)

def voeg_een_transactie_toe():
    print("We hebben deze functie nog niet uitgewerkt. Onze excuses.")

def exporteer_de_transacties_naar_csv():
    print("Het exporteren van de transacties naar csv is niet niet uitgewerkt")

def programma_verlaten():
    sys.exit(0)


def menu():
    print(
"""
1. Toon alle transacties
2. Voeg een transactie toe.
3. Exporteer alle transacties naar een csv-bestand.
4. Verlaat het programma.
""")
    keuze_succesvol = False
    while not keuze_succesvol:
        try:
            keuze = int(input("Geef het nummer van je keuze: "))
            print(f"Dit was je keuze: {keuze}")
            if keuze in (1, 2, 3, 4):
                keuze_succesvol = True
                print("Goede keuze")
            else:
                print("Je moet een getal van 1 tot 4 ingeven.")
        except ValueError:
            print("Je moet een geheel getal van 1 tot 4 ingeven.")
    if keuze == 1:
        toon_alle_transacties()
    elif keuze == 2:
        voeg_een_transactie_toe()
    elif keuze == 3:
        exporteer_de_transacties_naar_csv()
    else:
        programma_verlaten()
