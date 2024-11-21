import ollama

# Chat mit dem Modell starten
response = ollama.chat(
    model='llama3.2-vision',
    messages=[{
        'role': 'user',
        'content': 'Was ist auf diesem Bild zu sehen?',
        'images': ['/home/luna/Bilder/a_drawing_of_a_boy.jpg']  # Pfad zu deinem Bild
    }]
)

# Antwort ausgeben
print(response)
