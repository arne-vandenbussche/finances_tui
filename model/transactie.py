from datetime import date
import logging

class Transactie():
    def __init__(self, id:int = 0, datum: date = date.today(),
                 bedrag: float = 0.0, betaalwijze: str = "",
                 rekeningnummer: str = "", van_aan: str = "",
                 beschrijving: str = "", factuurnummer: str = "",
                 factuurdatum: date = date.today(), categorie: str = "",
                 actuele_rekeningstand: float = 0.0):
        if id is None:
            self.id = 0
        else:
            self.id = id
        if datum is None:
            self.datum = date.today()
        else:
            self.datum = datum
        if bedrag is None:
            self.bedrag = 0.0
        else:
            self.bedrag = bedrag
        if betaalwijze is None:
            self.betaalwijze = ""
        else:
            self.betaalwijze = betaalwijze
        if rekeningnummer is None:
            self.rekeningnummer = ""
        else:
            self.rekeningnummer = rekeningnummer
        if van_aan is None:
            self.van_aan = ""
        else:
            self.van_aan = van_aan
        if beschrijving is None:
            self.beschrijving = ""
        else:
            self.beschrijving = beschrijving
        if factuurnummer is None:
            self.factuurnummer = ""
        else:
            self.factuurnummer = factuurnummer
        if factuurdatum is None:
            self.factuurdatum = date.today()
        else:
            self.factuurdatum = factuurdatum
        if categorie is None:
            self.categorie = ""
        else:
            self.categorie = categorie
        if actuele_rekeningstand is None:
            self.actuele_rekeningstand = 0.0
        else:
            self.actuele_rekeningstand = actuele_rekeningstand

    def __str__(self):
        return f"Datum: {self.datum}. Bedrag: {self.bedrag}. Beschrijving: {self.beschrijving}"
