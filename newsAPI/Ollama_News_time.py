import requests
import sqlite3
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
        "give me the time",
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
    for keyword in time_keywords:
        if keyword in user_prompt.lower():
            return True
    return False

# Funktion zur Überprüfung, ob der Benutzer nach den Nachrichten fragt
def is_news_query(user_prompt: str):
    news_keywords = [
        "news", 
        "latest news", 
        "current news", 
        "headlines", 
        "what's in the news", 
        "tell me the news", 
        "any updates", 
        "any news updates"
    ]
    for keyword in news_keywords:
        if keyword in user_prompt.lower():
            return True
    return False

# Funktion zum Abrufen der neuesten Nachrichten aus der SQLite-Datenbank
def get_latest_news_from_db():
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()

    # Neuesten Nachrichten-Einträge abrufen (limit auf 3 gesetzt)
    cursor.execute('''
        SELECT title, description, source, published_at 
        FROM News 
        ORDER BY published_at DESC 
        LIMIT 3
    ''')
    latest_news = cursor.fetchall()
    conn.close()

    if latest_news:
        news_str = "\n".join([f"Title: {title}\nDescription: {description}\nSource: {source}\nPublished At: {published_at}\n" 
                              for title, description, source, published_at in latest_news])
        return news_str
    else:
        return "No news found."

# Funktion zum Abfragen des Ollama-Modells mit Zeit- und Nachrichtenintegration
def query_ollama_with_time_and_news(model: str, user_prompt: str):
    modified_prompt = user_prompt
    
    # Überprüfen, ob der Benutzer nach der Zeit fragt
    if is_time_query(user_prompt):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        modified_prompt = f"The current time is {current_time}. {modified_prompt}"

    # Überprüfen, ob der Benutzer nach den Nachrichten fragt
    if is_news_query(user_prompt):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        modified_prompt = f"The current time is {current_time}. {modified_prompt}"
        latest_news = get_latest_news_from_db()
        modified_prompt = f"The latest news is (please note that some might be outdated if they are make a note):\n{latest_news}\n{modified_prompt}"

    # Anfrage an Ollama
    url = "http://localhost:11434/v1/completions"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "prompt": modified_prompt
    }

    response = requests.post(url, json=payload, headers=headers)

    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        response_json = response.json()
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
        
        if user_input.lower() == "#bye#":
            break
        
        print("Ollama: ", end="")
        result = query_ollama_with_time_and_news("llama3.1", user_input)
        print(result)

# Programm starten
if __name__ == "__main__":
    main()
