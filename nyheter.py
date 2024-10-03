import requests
import pandas as pd
from datetime import datetime
from dateutil import parser
import pytz
import os

# API-endpoint för att hämta nyheter
url = "https://polisen.se/api/events"

# Hämta nuvarande händelser från API
response = requests.get(url)

if response.status_code == 200:
    events = response.json()

    # Skapa en tidszonsmedveten (offset-aware) version av end_date
    stockholm_tz = pytz.timezone('Europe/Stockholm')
    end_date = stockholm_tz.localize(datetime.today())

    # Kolla om en CSV-fil redan finns med tidigare data
    file_path = 'C:/Users/musta/OneDrive/Skrivbord/webb/stockholm_polisen_handelser.csv'
    file_exists = os.path.exists(file_path)

    if file_exists:
        # Läs in befintliga händelser från CSV
        existing_df = pd.read_csv(file_path)
        existing_dates = pd.to_datetime(existing_df['Datum'])

        # Datumet för den senaste händelsen i CSV-filen
        latest_existing_date = existing_dates.max()
    else:
        # Om filen inte finns, sätt en väldigt gammal startdatum
        latest_existing_date = stockholm_tz.localize(datetime(1900, 1, 1))

    # Lista för att lagra nya händelser
    new_events = []

    # Filtrera händelser som är nyare än den senaste sparade händelsen
    for event in events:
        try:
            event_date = parser.parse(event['datetime'])

            # Kontrollera om händelsen är nyare än den senaste sparade händelsen
            if event_date > latest_existing_date and "Stockholm" in event['location']['name']:
                new_events.append([
                    event['datetime'],
                    event['name'],
                    event['summary'],
                    event['location']['name'],
                    event['url']
                ])
        except ValueError as e:
            print(f"Fel vid datumparsning: {e}")

    # Om vi hittade några nya händelser, lägg till dem i CSV-filen
    if new_events:
        new_df = pd.DataFrame(new_events, columns=["Datum", "Rubrik", "Beskrivning", "Plats", "Länk"])

        # Om filen redan existerar, lägg till nya rader
        if file_exists:
            new_df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            # Skapa en ny fil om det är första körningen
            new_df.to_csv(file_path, index=False)

        print(f"Lade till {len(new_events)} nya händelser.")
    else:
        print("Inga nya händelser hittades.")
else:
    print(f"API-anropet misslyckades med statuskod: {response.status_code}")
