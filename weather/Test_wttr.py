import requests
import os
import json

# Funktion zum Überprüfen, ob der Raspberry Pi mit Strom versorgt wird
def is_powered():
    # Hier könntest du eine Logik implementieren, um den Stromstatus zu überprüfen.
    # Zum Beispiel: Überprüfen eines bestimmten GPIO-Pins, der signalisiert, ob Strom vorhanden ist.
    return True  # Für jetzt nehmen wir an, dass der Pi immer mit Strom versorgt wird.

# Funktion zum Abrufen der Wetterdaten von wttr.in
def fetch_weather_data():
    try:
        response = requests.get('https://wttr.in?format=j1')
        if response.status_code == 200:
            return response.json()  # Rückgabe der Wetterdaten als JSON
        else:
            print(f"Fehler beim Abrufen der Wetterdaten: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return None

# Funktion zum Speichern der Wetterdaten in einer Datei
def save_weather_data(data):
    try:
        with open('weather_data.json', 'w') as f:
            json.dump(data, f, indent=4)
        print("Wetterdaten erfolgreich gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern der Wetterdaten: {e}")

# Hauptlogik
if __name__ == "__main__":
    if is_powered():
        print("Der Raspberry Pi ist mit Strom versorgt.")
        weather_data = fetch_weather_data()
        if weather_data:
            save_weather_data(weather_data)
    else:
        print("Der Raspberry Pi ist nicht mit Strom versorgt.")
