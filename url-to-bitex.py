import requests
from bs4 import BeautifulSoup
import json

def extract_metadata(url):
    """
    Extrahiert Metadaten von der angegebenen URL.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"Fehler beim Abrufen der URL: {e}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Titel extrahieren
    title_tag = soup.find('title')
    title = title_tag.text.strip() if title_tag else 'Titel nicht gefunden'
    
    # Autoren extrahieren (Versuche verschiedene Methoden)
    author = 'Autor nicht gefunden'
    # Methode 1: Meta-Tag
    meta_author = soup.find('meta', attrs={'name': 'author'})
    if meta_author and meta_author.get('content'):
        author = meta_author['content'].strip()
    else:
        # Methode 2: Artikelautor in sichtbaren Tags (z.B. <a>, <span>)
        possible_author_tags = soup.find_all(['a', 'span'], attrs={'class': lambda x: x and 'author' in x.lower()})
        if possible_author_tags:
            author = possible_author_tags[0].get_text().strip()
    
    # Veröffentlichungsdatum extrahieren
    year = 'Jahr nicht gefunden'
    # Methode 1: Meta-Tag
    meta_date = soup.find('meta', attrs={'name': 'date'})
    if meta_date and meta_date.get('content'):
        year = meta_date['content'][:4]
    else:
        # Methode 2: Sichtbare Datumsangaben
        possible_date_tags = soup.find_all(['time', 'span'], attrs={'class': lambda x: x and 'date' in x.lower()})
        if possible_date_tags:
            date_text = possible_date_tags[0].get_text().strip()
            year = ''.join(filter(str.isdigit, date_text))[:4] if any(char.isdigit() for char in date_text) else 'Jahr nicht gefunden'
    
    return {
        'title': title,
        'author': author,
        'year': year,
        'url': url
    }

def generate_bibtex_with_ollama(metadata, ollama_api_key):
    """
    Generiert einen BibTeX-Eintrag mithilfe der Ollama API.
    """
    prompt = f"""
    Erstelle einen BibTeX-Eintrag mit den folgenden Informationen:

    Titel: {metadata['title']}
    Autoren: {metadata['author']}
    Jahr: {metadata['year']}
    URL: {metadata['url']}
    """
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ollama_api_key}'
    }
    
    data = {
        'model': 'llama3.2',  # Stelle sicher, dass das Modell korrekt ist
        'prompt': prompt,
        'max_tokens': 150,
        'temperature': 0.3
    }
    
    try:
        response = requests.post('http://localhost:11434/api/generate', headers=headers, data=json.dumps(data))
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"Fehler bei der Anfrage an Ollama: {e}")
    
    result = response.json()
    
    # Annahme: Die Antwortstruktur enthält 'choices' mit 'text'
    if 'choices' in result and len(result['choices']) > 0 and 'text' in result['choices'][0]:
        bibtex = result['choices'][0]['text'].strip()
        return bibtex
    else:
        raise Exception("Unerwartetes Antwortformat von Ollama.")

def main():
    """
    Hauptfunktion des Programms.
    """

    
    try:
        metadata = extract_metadata(url)
        print("\nMetadaten extrahiert:")
        for key, value in metadata.items():
            print(f"{key.capitalize()}: {value}")
        
        bibtex = generate_bibtex_with_ollama(metadata, ollama_api_key)
        print("\nGenerierter BibTeX-Eintrag:")
        print(bibtex)
        
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    main()
