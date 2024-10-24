import os
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from datetime import datetime
import torch
from diffusers import DiffusionPipeline
import requests

app = Flask(__name__)
CORS(app)  # CORS für Cross-Origin-Anfragen aktivieren
IMAGE_FOLDER = "static/images"  # Ordner, in dem die generierten Bilder gespeichert werden

OLLAMA_API_URL = 'http://localhost:11434/v1/completions'  # Ollama API-URL

# Stelle sicher, dass der Bildordner existiert
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# Funktion zur Bildgenerierung
def generate_image(prompt):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("\nLade das Stable Diffusion Modell...")
    pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1-base").to(device)

    print("Generiere das Bild...")
    image = pipe(prompt).images[0]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_image_{timestamp}.png"
    filepath = os.path.join(IMAGE_FOLDER, filename)

    image.save(filepath)  # Speichere das Bild im gewünschten Verzeichnis
    print(f"\nBild erfolgreich gespeichert: {filepath}")

    return filename

# Funktion zur Anfrage an die Ollama-API
def ask_ollama(prompt, model):
    try:
        # Daten für die POST-Anfrage an Ollama vorbereiten
        data = {
            "model": model,  # Das Modell wird dynamisch festgelegt
            "prompt": prompt
        }
        headers = {
            "Content-Type": "application/json"
        }
        # Anfrage an die Ollama-API senden
        response = requests.post(OLLAMA_API_URL, json=data, headers=headers)
        
        # Überprüfen, ob die Anfrage erfolgreich war
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Fehler bei der Ollama-Anfrage"}
    except Exception as e:
        return {"error": str(e)}

# Endpunkt zur Bildgenerierung
@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "Kein Prompt angegeben!"}), 400

    try:
        filename = generate_image(prompt)
        return jsonify({"filename": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpunkt für die Ollama-Abfrage
@app.route('/ask_ollama', methods=['POST'])
def ask_ollama_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    model = data.get('model', 'llama3.2:1b')  # Standardmäßig das Modell "llama3.2:1b"

    if not prompt:
        return jsonify({"error": "Kein Prompt angegeben!"}), 400

    # Anfrage an Ollama senden
    response = ask_ollama(prompt, model)

    # Antwort an den Client zurückgeben
    return jsonify(response)

# Endpunkt zur Bereitstellung aller Bilder in der Galerie (neueste zuerst)
@app.route('/gallery', methods=['GET'])
def gallery():
    try:
        # Liste aller Bilddateien im Ordner abrufen und nach Erstellungsdatum sortieren
        images = sorted(os.listdir(IMAGE_FOLDER), key=lambda x: os.path.getmtime(os.path.join(IMAGE_FOLDER, x)), reverse=True)
        return jsonify(images)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpunkt zum Abrufen einzelner Bilder aus dem statischen Ordner
@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
