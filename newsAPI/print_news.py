import sqlite3
from datetime import datetime

# Funktion zum Formatieren der Ausgabe
def print_news(title, description, url, published_at, source):
    print("="*80)
    print(f"Title: {title}")
    print(f"Source: {source}")
    print(f"Published At: {published_at}")
    print("-"*80)
    if description:
        print(f"Description: {description}")
    else:
        print("No description available.")
    print(f"Read more: {url}")
    print("="*80)
    print("\n")

# Funktion, um Nachrichten aus der SQLite-Datenbank zu holen und anzuzeigen
def show_news():
    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()

    # Nachrichten aus der Datenbank abrufen (maximal 10)
    cursor.execute('''
        SELECT title, description, url, published_at, source
        FROM News
        ORDER BY published_at DESC
    ''')
    
    rows = cursor.fetchall()

    if rows:
        print(f"Displaying {len(rows)} latest news articles:\n")
        for row in rows:
            title, description, url, published_at, source = row
            # Ausgabe der Nachrichten
            print_news(title, description, url, published_at, source)
    else:
        print("No news found in the database.")

    conn.close()

# Hauptfunktion zur Anzeige
if __name__ == "__main__":
    show_news()
