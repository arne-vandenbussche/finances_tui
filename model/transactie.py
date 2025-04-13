from datetime import date

class Transactie():
    def __init__(self, id: int = 0, datum: date = date.today(), 
                 bedrag: float = 0.0, betaalwijze: str = "", 
                 rekeningnummer: str = "", van_aan: str = "", 
                 beschrijving: str = "", factuurnummer: str = "", 
                 factuurdatum: date = date.today(), categorie: str = "", 
                 actuele_rekeningstand: float = 0.0):
        self.datum = datum
        self.bedrag = bedrag
        self.betaalwijze = betaalwijze
        self.rekeningnummer = rekeningnummer
        self.van_aan = van_aan
        self.beschrijving = beschrijving
        self.factuurnummer = factuurnummer
        self.factuurdatum = factuurdatum
        self.categorie = categorie
        self.actuele_rekeningstand = actuele_rekeningstand
        
    def __str__(self):
        return f"Datum: {self.datum}. Beschrijving: {self.beschrijving}"
        