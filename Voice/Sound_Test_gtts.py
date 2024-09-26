from gtts import gTTS
import os

# Funktion für Text-zu-Sprache mit gTTS
def speak(text):
    tts = gTTS(text=text, lang='de')
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")

# Beispiel für die Nutzung der speak-Funktion
speak("Hallo, how can I assist you today?")
