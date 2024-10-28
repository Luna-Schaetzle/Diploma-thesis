import os
import time
import pyaudio
import speech_recognition as sr
import pygame  # Neu hinzugefügt
from gtts import gTTS
import requests
import json
import uuid

lang = 'en'

def get_ollama_response(prompt):
    url = 'http://localhost:11434/api/generate'
    headers = {'Content-Type': 'application/json'}
    data = {
        'model': 'llama3.2:1b',
        'prompt': prompt
    }
    response = requests.post(url, headers=headers, json=data, stream=True)
    if response.status_code == 200:
        text = ''
        for line in response.iter_lines():
            if line:
                json_data = json.loads(line.decode('utf-8'))
                text += json_data.get('response', '')
        return text
    else:
        print(f"Error: {response.status_code}")
        return ''

def play_audio(file_name):
    pygame.mixer.init()
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()

def get_audio():
    global guy
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
            guy = said

            if "Jarvis" in said:
                new_string = said.replace("Jarvis", "").strip()
                print(new_string)
                text = get_ollama_response(new_string)
                speech = gTTS(text=text, lang=lang, slow=False, tld="com.au")
                file_name = f"response_{str(uuid.uuid4())}.mp3"
                speech.save(file_name)
                play_audio(file_name)

        except Exception as e:
            print(f"Exception: {str(e)}")

    return said

guy = ""

while True:
    if "stop" in guy:
        break

    get_audio()
