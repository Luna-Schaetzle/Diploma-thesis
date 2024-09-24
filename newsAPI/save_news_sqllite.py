import requests
import sqlite3
from datetime import datetime

# API-Schlüssel und Endpunkt der NewsAPI
API_KEY = '1a204d2b61214f0f8c80f6a8b8107cbd'
NEWS_URL = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}'

# Funktion zum Abrufen der Nachrichten
def fetch_news():
    response = requests.get(NEWS_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching news: {response.status_code}")
        return None

# Funktion zum Erstellen der SQLite-Datenbank und Tabelle
def create_database():
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()

    # Tabelle erstellen, wenn sie nicht existiert
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS News (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            url TEXT,
            published_at TEXT,
            source TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Funktion zum Speichern der Nachrichten in der Datenbank
def save_news_to_db(articles):
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()

    for article in articles:
        title = article.get('title')

         # Prüfen, ob der Titel '[Removed]' enthält
        if title == '[Removed]':
            print(f"Skipping article with title '[Removed]': {article.get('url')}")
            continue  # Überspringt den Eintrag


        description = article.get('description')
        url = article.get('url')
        published_at = article.get('publishedAt')
        source = article['source'].get('name')

        # Nur neue Nachrichten speichern, doppelte Einträge vermeiden
        cursor.execute('''
            SELECT COUNT(*) FROM News WHERE title = ? AND published_at = ?
        ''', (title, published_at))
        result = cursor.fetchone()

        if result[0] == 0:
            cursor.execute('''
                INSERT INTO News (title, description, url, published_at, source)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, description, url, published_at, source))

    conn.commit()
    conn.close()

# Funktion, um den gesamten Ablauf zu steuern
def main():
    # 1. Datenbank erstellen
    create_database()

    # 2. Nachrichten abrufen
    news_data = fetch_news()

    if news_data:
        articles = news_data.get('articles')
        if articles:
            print(f"Fetched {len(articles)} articles.")
            # 3. Nachrichten in der Datenbank speichern
            save_news_to_db(articles)
        else:
            print("No articles found.")
    else:
        print("Failed to fetch news.")

if __name__ == "__main__":
    main()
