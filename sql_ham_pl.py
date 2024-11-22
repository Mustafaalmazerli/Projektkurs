import requests
import pandas as pd
from datetime import datetime
from dateutil import parser
import pytz
import pyodbc
import random

# API
url = "https://polisen.se/api/events"

# Anslut till SQL Server
def connect_to_sql_server():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=.........;' 
        'DATABASE=............;'
        'Trusted_Connection=yes;'
    )
    return conn


#  Latitude och Longitude baserat på plats
def generate_random_coordinates(location):
    cities = {
        "Stockholm": (59.3293, 18.0686),
    "Malmö": (55.6050, 13.0038),
    "Göteborg": (57.7089, 11.9746),
    "Uppsala": (59.8586, 17.6389),
    "Örebro": (59.2741, 15.2066),
    "Linköping": (58.4108, 15.6214),
    "Helsingborg": (56.0465, 12.6945),
    "Lund": (55.7047, 13.1910),
    "Umeå": (63.8258, 20.2630),
    "Gävle": (60.6749, 17.1413),
    "Eskilstuna": (59.3666, 16.5077),
    "Halmstad": (56.6745, 12.8570),
    "Borås": (57.7210, 12.9401),
    "Södertälje": (59.1955, 17.6253),
    "Västerås": (59.6162, 16.5528),
    "Karlstad": (59.3793, 13.5036),
    "Sundsvall": (62.3908, 17.3069),
    "Trollhättan": (58.2837, 12.2886),
    "Kalmar": (56.6634, 16.3567),
    "Skövde": (58.3912, 13.8458),
    "Luleå": (65.5848, 22.1547),
    "Trelleborg": (55.3751, 13.1579),
    "Kristianstad": (56.0313, 14.1526),
    "Växjö": (56.8777, 14.8090),
    "Jönköping": (57.7826, 14.1600),
    "Norrköping": (58.5877, 16.1924),
    "Karlskrona": (56.1612, 15.5869),
    "Falun": (60.6030, 15.6253),
    "Nyköping": (58.7530, 17.0083),
    "Kiruna": (67.8558, 20.2253),
    "Motala": (58.5371, 15.0364),
    "Västervik": (57.7584, 16.4487),
    "Hudiksvall": (61.7285, 17.1046),
    "Falkenberg": (56.9050, 12.4910),
    "Lidköping": (58.5085, 13.1577),
    "Åre": (63.3985, 13.0827),
    "Piteå": (65.3172, 21.4793),
    "Alingsås": (57.9301, 12.5336),
    "Sigtuna": (59.6157, 17.7234),
    "Ystad": (55.4297, 13.8200),
    "Sollefteå": (63.1660, 17.2718),
    "Ängelholm": (56.2428, 12.8622),
    "Vänersborg": (58.3803, 12.3239),
    "Mariestad": (58.7071, 13.8234),
    "Östersund": (63.1792, 14.6357),
    "Borlänge": (60.4856, 15.4371),
    "Arvika": (59.6544, 12.5854),
    "Visby": (57.6348, 18.2948),
    "Landskrona": (55.8708, 12.8304),
    "Värnamo": (57.1860, 14.0404),
    "Ljungby": (56.8311, 13.9400),
    "Fagersta": (60.0045, 15.7930),
    "Kramfors": (62.9272, 17.7759),
    "Boden": (65.8252, 21.6886),
    "Sandviken": (60.6172, 16.7755),
    "Åmål": (59.0520, 12.6992),
    "Torsby": (60.1375, 13.0036),
    "Eksjö": (57.6657, 14.9738),
    "Säffle": (59.1326, 12.9274),
    "Höör": (55.9376, 13.5423),
    "Sala": (59.9226, 16.6062),
    "Avesta": (60.1453, 16.1679),
    "Båstad": (56.4280, 12.8465)
    }

    if location in cities:
        base_lat, base_lon = cities[location]
    else:
        # Om platsen inte matchar någon av dessa, välj en slumpmässig stad
        city = random.choice(list(cities.keys()))
        base_lat, base_lon = cities[city]

    # avvikelse för att simulera närliggande områden
    lat_offset = random.uniform(-0.05, 0.05)
    lon_offset = random.uniform(-0.05, 0.05)

    return base_lat + lat_offset, base_lon + lon_offset

# ta bort datum och plats från rubriken
def clean_rubrik(event_name):
    
    if "," in event_name:
        parts = event_name.split(',')  
        if len(parts) > 2:
            return parts[1].strip()  
        elif len(parts) > 1:
            return parts[1].strip()  
    return event_name 

# spara en brottshändelse i SQL-databasen
def save_crime_event(conn, event_date, event_name, latitude, longitude, location, link):
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO CrimeEvents (EventDate, EventName, Latitude, Longitude, Location, Link)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    
    cursor.execute(insert_query, (event_date, event_name, latitude, longitude, location, link))
    conn.commit()

# Hämta brottshändelser från API och lägg till dem i SQL-databasen
def fetch_and_store_events():
    # Hämta data från API
    response = requests.get(url)

    if response.status_code == 200:
        events = response.json()

        # Skapa en tidszonsmedveten version av nuvarande tid
        stockholm_tz = pytz.timezone('Europe/Stockholm')
        end_date = stockholm_tz.localize(datetime.today())

        # jämföra data från SQL-databasen för att kontrollera senaste händelse
        conn = connect_to_sql_server()
        cursor = conn.cursor()

        # Hämta den senaste händelsens datum från databasen
        cursor.execute("SELECT MAX(EventDate) FROM CrimeEvents")
        latest_existing_date = cursor.fetchone()[0]

        if latest_existing_date is None:
            # Om det inte finns någon händelse i databasen, sätt en gammal datum
            latest_existing_date = stockholm_tz.localize(datetime(1900, 1, 1))

        # Lista för nya händelser
        new_events = []

        # Filtrera och bearbeta nya händelser
        for event in events:
            try:
                event_date = parser.parse(event['datetime'])

                # Gör både event_date och latest_existing_date till offset-naive 
                event_date_naive = event_date.replace(tzinfo=None)
                latest_existing_date_naive = latest_existing_date.replace(tzinfo=None)

                # Kontrollera om händelsen är nyare än den senaste händelsen i databasen
                if event_date_naive > latest_existing_date_naive:
                    location = event['location']['name']
                    event_name = clean_rubrik(event['name'])  
                    link = event['url']
                    description = event.get('summary', '')

                    # Generera latitud och longitud
                    latitude, longitude = generate_random_coordinates(location)

                    # Spara händelsen i SQL Server
                    save_crime_event(conn, event_date, event_name, latitude, longitude, location, link)

                    new_events.append({
                        'event_date': event_date,
                        'event_name': event_name,
                        'location': location,
                        'latitude': latitude,
                        'longitude': longitude,
                        'link': link
                    })

            except ValueError as e:
                print(f"Fel vid datumparsning: {e}")

        # Stäng anslutningen till databasen
        cursor.close()
        conn.close()

        # Ge feedback om nya händelser som lagts till
        if new_events:
            print(f"Lade till {len(new_events)} nya händelser.")
        else:
            print("Inga nya händelser hittades.")
    else:
        print(f"API-anropet misslyckades med statuskod: {response.status_code}")

# Kör funktionen för att hämta och spara brottshändelser
fetch_and_store_events()
