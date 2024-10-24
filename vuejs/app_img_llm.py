import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import requests

app = Flask(__name__)
CORS(app)

OLLAMA_API_URL = 'http://localhost:11434/v1/completions'

@app.route('/send_image_prompt', methods=['POST'])
def send_image_prompt():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        image_base64 = data.get('image')

        if not prompt or not image_base64:
            return jsonify({"error": "Bild und Prompt dürfen nicht leer sein!"}), 400

        # Anfrage an die Ollama-API senden
        response = requests.post(OLLAMA_API_URL, json={
            "model": "llava",
            "prompt": prompt,
            "images": [image_base64]  # Base64-kodiertes Bild mitsenden
        })

        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Fehler bei Ollama: {response.text}"}), response.status_code

    except Exception as e:
        return jsonify({"error": f"Serverfehler: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
