import speech_recognition as sr

# Initialisiere den Recognizer
recognizer = sr.Recognizer()

def listen():
    # Mikrofon als Quelle verwenden
    with sr.Microphone() as source:
        print("Bitte sprechen...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            # Offline-Erkennung mit Sphinx
            text = recognizer.recognize_sphinx(audio)
            print(f"Du hast gesagt: {text}")
            return text
        except sr.UnknownValueError:
            print("Entschuldigung, ich konnte dich nicht verstehen.")
        except sr.RequestError:
            print("Es gab ein Problem mit dem Service.")

if __name__ == "__main__":
    while True:
        command = listen()
        if command == "exit":
            break
