import requests
import pandas as pd
from datetime import datetime
from dateutil import parser
import pytz  # För att hantera tidszoner

# Hämta händelser från polisens API
url = "https://polisen.se/api/events"
response = requests.get(url)

# Kontrollera om anropet lyckades
if response.status_code == 200:
    events = response.json()

    # Lista för att lagra händelser
    events_data = []

    # Skapa en tidszonsmedveten (offset-aware) version av start_date och end_date
    stockholm_tz = pytz.timezone('Europe/Stockholm')  # Stockholm tidszon
    start_date = stockholm_tz.localize(datetime(2024, 9, 2))  # Offset-aware start date
    end_date = stockholm_tz.localize(datetime.today())  # Offset-aware end date

    # Loopa igenom alla händelser och filtrera på datum och plats
    for event in events:
        try:
            # Använd parser för att hantera tidszonen korrekt
            event_date = parser.parse(event['datetime'])

            # Filtrera på datum och plats
            if start_date <= event_date <= end_date and "Stockholm" in event['location']['name']:
                events_data.append([
                    event['datetime'],
                    event['name'],
                    event['summary'],
                    event['location']['name'],
                    event['url']
                ])
        except ValueError as e:
            print(f"Fel vid datumparsning: {e}")

    # Skapa en DataFrame från händelsedatan
    df = pd.DataFrame(events_data, columns=["Datum", "Rubrik", "Beskrivning", "Plats", "Länk"])

    # Spara till CSV
    df.to_csv('stockholm_polisen_handelser.csv', index=False)

    print(f"Händelser har sparats till 'stockholm_polisen_handelser.csv'.")
else:
    print(f"API-anropet misslyckades med statuskod: {response.status_code}")
