import subprocess

def speak(text):
    subprocess.run(['festival', '--tts'], input=text, text=True)

speak("Hello, how can I assist you today?")
