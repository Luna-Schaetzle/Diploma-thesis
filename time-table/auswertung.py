import csv
from collections import defaultdict
import os

def parse_time(time_str):
    try:
        parts = list(map(int, time_str.split(':')))
        h, m, s = (parts + [0, 0])[:3]  # Ergänzt fehlende Teile mit 0
        return h * 60 + m + s / 60  # Rückgabe in Minuten
    except ValueError:
        raise ValueError(f"Ungültiges Zeitformat: {time_str}")

def calculate_working_hours(csv_file):
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"Datei nicht gefunden: {csv_file}")
    
    working_hours = defaultdict(float)

    with open(csv_file, newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        headers = next(reader, None)  # Header lesen, falls vorhanden
        
        for row in reader:
            try:
                time_str = row[3]  # 'working hours' column
                persons = row[6].split(', ')  # Split multiple names
                
                time_in_minutes = parse_time(time_str)
                
                for person in persons:
                    working_hours[person.strip()] += time_in_minutes / 60  # Convert to hours
            except IndexError:
                print(f"Fehlerhafte Zeile übersprungen: {row}")
    
    return working_hours

def main():
    csv_file = 'arbeitszeit-1.csv'  # Datei mit der Tabelle
    try:
        hours = calculate_working_hours(csv_file)
        for person, total_hours in sorted(hours.items()):
            print(f"{person}: {total_hours:.2f} Stunden")
    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    main()
