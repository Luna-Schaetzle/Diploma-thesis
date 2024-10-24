from flask import Flask, request, jsonify, send_from_directory
import os
import torch
from diffusers import DiffusionPipeline
from PIL import Image
from datetime import datetime

app = Flask(__name__)

# Umgebungsvariable für CUDA-Speicherverwaltung setzen
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

# Lade das Stable Diffusion Modell beim Start
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1-base").to(device)

# Verzeichnis für generierte Bilder
IMAGE_DIR = 'generated_images'
os.makedirs(IMAGE_DIR, exist_ok=True)

@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({'error': 'Der Prompt darf nicht leer sein!'}), 400

    # Bild generieren
    image = pipe(prompt).images[0]

    # Eindeutigen Dateinamen erstellen
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_image_{timestamp}.png"
    filepath = os.path.join(IMAGE_DIR, filename)
    
    # Speichere das Bild im gewünschten Format
    image.save(filepath)
    
    return jsonify({'message': 'Bild erfolgreich gespeichert!', 'filename': filename})

@app.route('/images/<filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

@app.route('/images', methods=['GET'])
def list_images():
    files = os.listdir(IMAGE_DIR)
    return jsonify(files)

if __name__ == '__main__':
    app.run(debug=True)
