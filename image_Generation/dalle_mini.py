from dalle_mini import DalleBart, DalleBartProcessor
from transformers import DalleBartTokenizer

# Initialisiere Modell und Tokenizer
model = DalleBart.from_pretrained("dalle-mini/dalle-mini")
tokenizer = DalleBartTokenizer.from_pretrained("dalle-mini/dalle-mini")

# Beispiel: Bildgenerierung
text = "A futuristic city with flying cars"
inputs = tokenizer([text], return_tensors="pt")

generated_images = model.generate(**inputs)
