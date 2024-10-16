
INSERT INTO Subscribers (Email, Latitude, Longitude, RadiusKm)
VALUES
('user1@example.com', 59.3293, 18.0686, 5.0),   -- Stockholm
('user2@example.com', 59.8586, 17.6389, 10.0),  -- Uppsala
('user3@example.com', 57.7089, 11.9746, 15.0);  -- Göteborg
INSERT INTO Subscribers (Email, Latitude, Longitude, RadiusKm)
VALUES
('mustafaalmazerli@gmail.com', 56.6745, 12.8572, 20.0);  -- Halmstad

SELECT * FROM CrimeEvents;

DELETE FROM CrimeEvents
WHERE CrimeID BETWEEN 501 AND 560;


UPDATE CrimeEvents
SET EventName = LEFT(EventName, CHARINDEX(',', EventName) - 1)
WHERE CHARINDEX(',', EventName) > 0;
SELECT DISTINCT EventName
FROM CrimeEvents;


-- Lägg till en kolumn för brottskategori
ALTER TABLE CrimeEvents
ADD CrimeCategory NVARCHAR(50);

-- Uppdatera CrimeCategory baserat på brottstyp (EventName)
UPDATE CrimeEvents
SET CrimeCategory = CASE
    WHEN EventName IN ('Bråk', 'Misshandel', 'Rån', 'Våldtäkt', 'Mord/dråp', 'Våld/hot mot tjänsteman', 'Olaga hot', 'Skottlossning', 'Ofredande/förargelse', 'Knivlagen', 'Vapenlagen', 'Narkotikabrott') THEN 'Våldsbrott'
    WHEN EventName IN ('Stöld', 'Inbrott', 'Bedrägeri', 'Motorfordon', 'Skadegörelse', 'Åldringsbrott', 'Olaga intrång', 'Stöld/inbrott', 'Hemfridsbrott', 'Häleri') THEN 'Egendomsbrott'
    WHEN EventName IN ('Trafikbrott', 'Trafikkontroll', 'Trafikolycka', 'Trafikhinder', 'Rattfylleri', 'Olovlig körning') THEN 'Trafikrelaterade brott'
    WHEN EventName IN ('Anträffad död', 'Arbetsplatsolycka', 'Brand', 'Djur', 'Explosion', 'Farligt föremål', 'Fjällräddning', 'Fylleri/LOB', 'Försvunnen person', 'Kontroll person/fordon', 'Larm Inbrott', 'Polisinsats/kommendering', 'Sammanfattning kväll och natt', 'Sammanfattning natt', 'Övrigt') THEN 'Övriga incidenter'
    ELSE 'Okänd kategori'
END;

SELECT * 
from CrimeEvents;


-- Lägg till kolumn för tid på dagen
ALTER TABLE CrimeEvents
ADD TimeOfDay NVARCHAR(20);

-- Lägg till kolumn för veckodag
ALTER TABLE CrimeEvents
ADD Weekday NVARCHAR(20);

-- Uppdatera TimeOfDay och Weekday baserat på EventDate
UPDATE CrimeEvents
SET TimeOfDay = CASE
    WHEN DATEPART(HOUR, EventDate) BETWEEN 6 AND 12 THEN 'Morgon'
    WHEN DATEPART(HOUR, EventDate) BETWEEN 12 AND 18 THEN 'Eftermiddag'
    WHEN DATEPART(HOUR, EventDate) BETWEEN 18 AND 22 THEN 'Kväll'
    ELSE 'Natt'
END,
Weekday = DATENAME(WEEKDAY, EventDate);




select * 
from CrimeEvents;






