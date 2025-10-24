# Doel

Een kleine TUI-applicatie bouwen om financiële transacties van een vereniging bij te houden.

# Technologie

- Python (Vanaf 3.11)

# Bibliotheken
(zie requierements.txt)

- environs

# Uitwerkte functionaliteiten

- Toon alle transacties

# Op de planning

- Transactie toevoegen
- Transactie wijzigen
- Transactie verwijderen
- Export naar csv
- Filtermogelijkheden voorzien bij het tonen of exporteren van transacties
- UI verbeteren (introductie van Textual)

# Naam database

Voorzie in de hoofdmap een bestand met de naam `.env`. Voeg daarin de tekst:

```text
DATABASE=name_of_database
````
Vervang de naam van de database door de naam die je wil gebruiken.
Als de database nog niet bestaat, zal hij aangemaakt worden

# Hoe uitvoeren

1. Clone the repository of download de code

2. Maak een virtuele omgeving:

```bash
python -m venv .venv
```

3. Installeer de externe bibliotheken

```bash
pip install -r requiements.txt
```

4. Voer de code uit:

```
python -m main
```


