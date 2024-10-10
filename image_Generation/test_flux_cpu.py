import os
import torch
from diffusers import FluxPipeline

# Umgebungsvariablen setzen, um CPU-Threads zu beschränken
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

# Lade das Modell ohne GPU
pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.float16)


# Beispiel-Prompt
prompt = "Ein schönes Bild von einer Landschaft"

# Generiere das Bild mit reduzierten Einstellungen
try:
    with torch.no_grad():  # Gradientenspeicher deaktivieren
        image = pipe(prompt, num_inference_steps=5, guidance_scale=7.5, batch_size=1, height=128, width=128)
    image.save("output_image.png")  # Speichere das generierte Bild
except Exception as e:
    print(f"Ein Fehler ist aufgetreten: {e}")
