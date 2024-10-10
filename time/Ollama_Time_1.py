import requests
from datetime import datetime

# Funktion zur Überprüfung, ob der Benutzer nach der Zeit fragt
def is_time_query(user_prompt: str):
    time_keywords = [
        "what time is it", 
        "current time", 
        "can you tell me the time", 
        "what's the time", 
        "tell me the time", 
        "what is the time", 
        "do you know the time", 
        "time now", 
        "give me the time"
        "what's the current time",
        "could you tell me the time",
        "may I know the time",
        "time please",
        "what time do you have",
        "do you have the time",
        "tell me what time it is",
        "what is the current time",
        "can you give me the time"
    ]
    # Benutzer-Eingabe auf Zeitfragen überprüfen
    for keyword in time_keywords:
        if keyword in user_prompt.lower():
            return True
    return False

# Funktion zum Abfragen des Ollama-Modells mit oder ohne Zeit
def query_ollama_with_time(model: str, user_prompt: str):
    # Überprüfen, ob der Benutzer nach der Zeit fragt
    if is_time_query(user_prompt):
        # Aktuelle Zeit abfragen
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Den Prompt mit der aktuellen Zeit modifizieren
        modified_prompt = f"The current time is {current_time}. {user_prompt}"
    else:
        # Kein Zeitbezug, ursprünglicher Prompt wird verwendet
        modified_prompt = user_prompt

    url = "http://localhost:11434/v1/completions"  # API-Endpunkt von Ollama
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "prompt": modified_prompt  # Modifizierter Benutzer-Prompt (mit oder ohne Zeit)
    }

    # Anfrage senden
    response = requests.post(url, json=payload, headers=headers)

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

# Hauptschleife für die Benutzerinteraktion
def main():

    while True:
        print("You: ", end="")
        user_input = input()
        
        if user_input.lower() == "exit":
            break
        
        print("Ollama: ", end="")
        result = query_ollama_with_time("llama3.1", user_input)
        print(result)
        

# Programm starten
if __name__ == "__main__":
    main()
