import argparse
import base64
import os
import requests
import sys
import json
import logging

# Konfiguriere das Logging
logging.basicConfig(filename='llava_image_analyzer.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def encode_image_to_base64(image_path):
    try:
        with open(image_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_string
    except Exception as e:
        logging.error(f"Fehler beim Lesen oder Kodieren des Bildes: {e}")
        print(f"Fehler beim Lesen oder Kodieren des Bildes: {e}")
        sys.exit(1)

def send_request(image_base64, prompt="Was ist auf diesem Bild zu sehen?"):
    url = "http://localhost:11434/v1/completions"
    payload = {
        "model": "llava:13b",
        "prompt": prompt,
        "images": ['/home/luna/Bilder/Rei_Ayanami.jpg'] 
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        logging.info(f"Anfrage erfolgreich gesendet an {url}")
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Fehler bei der Kommunikation mit der LLaVA-API: {e}")
        print(f"Fehler bei der Kommunikation mit der LLaVA-API: {e}")
        sys.exit(1)

def parse_response(response):
    try:
        result = response.json()
        logging.info("Antwort erfolgreich als JSON geparst.")
    except json.JSONDecodeError as e:
        logging.error(f"Fehler beim Parsen der JSON-Antwort: {e}")
        print(f"Fehler beim Parsen der JSON-Antwort: {e}")
        sys.exit(1)

    if 'choices' in result and isinstance(result['choices'], list) and len(result['choices']) > 0:
        choice = result['choices'][0]
        if 'text' in choice:
            logging.info("Text aus den 'choices' extrahiert.")
            return choice['text'].strip()
        else:
            logging.warning("Das Feld 'text' ist in der ersten Wahl nicht vorhanden.")
    else:
        logging.warning("Das Feld 'choices' ist nicht vorhanden oder leer.")
    
    if 'response' in result:
        logging.info("Verwendung des 'response'-Feldes als Fallback.")
        return result['response']
    
    logging.error("Unerwartetes Antwortformat erhalten.")
    print("Unerwartetes Antwortformat:")
    print(json.dumps(result, indent=2))
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Sende ein Bild an LLaVA zur Analyse.")
    parser.add_argument('image_path', type=str, help='Pfad zur Bilddatei.')
    parser.add_argument('--prompt', type=str, default="Was ist auf diesem Bild zu sehen?", help='Prompt für die Bildanalyse.')

    args = parser.parse_args()
    image_path = args.image_path
    prompt = args.prompt

    if not os.path.isfile(image_path):
        logging.error(f"Die Datei '{image_path}' existiert nicht.")
        print(f"Die Datei '{image_path}' existiert nicht.")
        sys.exit(1)

    image_base64 = encode_image_to_base64(image_path)
    response = send_request(image_base64, prompt)

    # Parse die Antwort und gib das Ergebnis aus
    result_text = parse_response(response)
    print("\nLLaVA Antwort:")
    print(result_text)
    logging.info("Antwort erfolgreich ausgegeben.")

if __name__ == "__main__":
    main()
