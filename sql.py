import pyodbc
from datetime import datetime
import pandas as pd
import random
from dateutil import parser  

# ansluta till SQL 
def connect_to_sql_server():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=MUSTAF;' 
        'DATABASE=CrimeNotificationSystem;' 
        'Trusted_Connection=yes;'  
    )
    return conn
   
# rensa Rubrik 
def clean_rubrik(rubrik):
    
    parts = rubrik.split(',', 1)
    if len(parts) > 1:
        return parts[1].strip()  
    return rubrik

# Funktion för att generera Latitude och Longitude baserat på plats
def generate_random_coordinates(location):
    # Definiera kända städer och deras koordinater
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
        "Södertälje": (59.1955, 17.6253)
    }

    # Välj närmaste kända stad eller generera slumpmässiga värden om platsen är okänd
    if location in cities:
        base_lat, base_lon = cities[location]
    else:
        # Om platsen inte matchar någon av dessa, välj en slumpmässig stad
        city = random.choice(list(cities.keys()))
        base_lat, base_lon = cities[city]

    # Lägg till en liten avvikelse för att simulera närliggande områden
    lat_offset = random.uniform(-0.05, 0.05)
    lon_offset = random.uniform(-0.05, 0.05)

    return base_lat + lat_offset, base_lon + lon_offset

# Funktion för att infoga brottshändelser i SQL-databasen
def save_crime_event(conn, event_date, event_name, latitude, longitude, location, link):
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO CrimeEvents (EventDate, EventName, Latitude, Longitude, Location, Link)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    
    cursor.execute(insert_query, (event_date, event_name, latitude, longitude, location, link))
    conn.commit()

# Läs data från CSV-fil och ladda upp till SQL Server
def upload_crime_data_from_csv(csv_file_path):
    # Läs CSV-filen till en Pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Anslut till SQL Server
    conn = connect_to_sql_server()

    # Iterera över varje rad i DataFrame
    for index, row in df.iterrows():
        try:
            # Omvandla Datum till ett datetime-objekt
            event_date = parser.parse(row['Datum'])

            # Rensa Rubrik för att ta bort datum och tid
            event_name = clean_rubrik(row['Rubrik'])

            # Plats ska vara i Location
            location = row['Plats']

            # Hämta länk
            link = row['Länk']

            # Generera Latitude och Longitude baserat på plats
            latitude, longitude = generate_random_coordinates(location)

            # Spara brottshändelsen i SQL Server
            save_crime_event(conn, event_date, event_name, latitude, longitude, location, link)
        
        except Exception as e:
            print(f"Fel vid uppladdning av händelse på rad {index}: {e}")


    conn.close()

#  ladda upp data 
csv_file_path = 'C:/Users/musta/OneDrive/Skrivbord/projket/sverige_handelser.csv'
upload_crime_data_from_csv(csv_file_path)
