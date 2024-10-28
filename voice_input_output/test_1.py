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
    # (Unverändert)

def play_audio(file_name):
    # (Unverändert)

def list_microphones():
    print("Available microphone devices:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"Microphone with index {index}: {name}")

def get_audio():
    global guy
    r = sr.Recognizer()
    try:
        with sr.Microphone(device_index=None) as source:
            print("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = r.listen(source)
        said = r.recognize_google(audio)
        print(f"You said: {said}")
        guy = said

        if "Jarvis" in said:
            new_string = said.replace("Jarvis", "").strip()
            print(f"Processing command: {new_string}")
            text = get_ollama_response(new_string)
            speech = gTTS(text=text, lang=lang, slow=False, tld="com.au")
            file_name = f"response_{str(uuid.uuid4())}.mp3"
            speech.save(file_name)
            play_audio(file_name)

    except Exception as e:
        print(f"Exception: {str(e)}")

guy = ""

if __name__ == "__main__":
    list_microphones()
    while True:
        if "stop" in guy:
            break
        get_audio()
