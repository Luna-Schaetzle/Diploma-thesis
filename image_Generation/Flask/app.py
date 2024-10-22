import os
from datetime import datetime
import torch
from flask import Flask, request, render_template, send_from_directory
from diffusers import DiffusionPipeline
from PIL import Image

# Umgebungsvariable für CUDA-Speicherverwaltung setzen
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

# Initialisiere Flask
app = Flask(__name__)
output_folder = "generated_images"  # Ordner zum Speichern der Bilder

# Stelle sicher, dass der Ausgabeordner existiert
os.makedirs(output_folder, exist_ok=True)

# Funktion zur Bildgenerierung
def generate_image(prompt):
    # Stelle sicher, dass das Modell auf der CPU läuft (oder GPU, falls verfügbar)
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Lade das Stable Diffusion Modell
    print("\nLade das Stable Diffusion Modell...")
    pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1-base").to(device)

    # Bild generieren
    print("Generiere das Bild...")
    image = pipe(prompt).images[0]

    # Eindeutigen Dateinamen erstellen
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_image_{timestamp}.png"
    
    # Speichere das Bild im gewünschten Format
    image.save(os.path.join(output_folder, filename))  # Speichern als PNG
    print(f"\nBild erfolgreich gespeichert: {filename}")
    return filename

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    if prompt.strip():
        filename = generate_image(prompt)
        return render_template('result.html', filename=filename)
    else:
        return "Fehler: Der Prompt darf nicht leer sein!"

@app.route('/generated_images/<path:filename>')
def send_image(filename):
    return send_from_directory(output_folder, filename)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
