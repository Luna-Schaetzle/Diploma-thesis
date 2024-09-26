import subprocess

def speak(text):
    subprocess.run(['espeak', text])

speak("Hello, how can I assist you today?")
