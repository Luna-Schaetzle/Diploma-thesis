import requests
import threading
import time

# Ladeindikator-Funktion
def loading_indicator(stop_event):
    loading_symbols = ['|', '/', '-', '\\']
    idx = 0
    while not stop_event.is_set():
        print(f"\rProcessing {loading_symbols[idx]}", end="")
        idx = (idx + 1) % len(loading_symbols)
        time.sleep(0.2)
    print("\rDone!            ")  # Zeile nach dem Ende der Verarbeitung löschen

def query_ollama(model: str, prompt: str, stop_event):
    url = "http://localhost:11434/v1/completions"  # API-Endpunkt von Ollama
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "prompt": prompt
    }

    # Anfrage senden
    response = requests.post(url, json=payload, headers=headers)

    # Ladeindikator stoppen
    stop_event.set()

    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        response_json = response.json()
        # Das generierte Ergebnis befindet sich in choices[0]["text"]
        if "choices" in response_json and len(response_json["choices"]) > 0:
            return response_json["choices"][0]["text"]
        else:
            return "Error: No text found in response."
    else:
        return f"Error: {response.status_code} - {response.text}"

# Hauptschleife für Benutzereingabe und Ollama-Anfrage
while True:
    print("You: ", end="")
    question = input()
    if question == "exit":
        break

    # Ladeindikator-Thread starten
    stop_event = threading.Event()
    loading_thread = threading.Thread(target=loading_indicator, args=(stop_event,))
    loading_thread.start()

    # Anfrage an Ollama senden
    result = query_ollama("llama3.1", question, stop_event)

    # Ladeindikator-Thread stoppen, sobald die Antwort vorliegt
    loading_thread.join()

    # Antwort ausgeben
    print(f"Ollama: {result}")
