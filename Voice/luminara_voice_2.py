import ollama
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import simpleaudio as sa
from pynput import keyboard  # Neue Bibliothek für Tastendrucküberwachung

# Read the character sheet from a file
with open("charactersheet.txt", "r") as file:
    information = file.read()

recording = False  # Flag, um den Aufnahmezustand zu verfolgen

# Define a function to interact with the local Ollama model
def chat_with_ollama(prompt, max_tokens=50):
    response = ollama.chat(
        model="llama2",  # Ersetze dies mit dem Namen deines Ollama-Modells
        messages=[
            {"role": "system", "content": information},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens
    )
    return response['choices'][0]['message']['content']

# Function to convert text to speech and save it as an MP3 file
def text_to_speech(text, mp3_file):
    tts = gTTS(text, lang='en')
    tts.save(mp3_file)

# Function to play the MP3 file
def play_mp3(mp3_file):
    audio = AudioSegment.from_mp3(mp3_file)
    playback_obj = sa.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
    playback_obj.wait_done()

# Function to record speech from the user
def record_user_speech():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Recording now! Speak...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise

        try:
            audio = recognizer.listen(source, timeout=5)  # Record audio for up to 5 seconds
            user_input = recognizer.recognize_google(audio)  # Recognize speech using Google Speech Recognition
            print(f"You (recorded): {user_input}")
            return user_input
        except sr.UnknownValueError:
            print("No speech detected or couldn't understand the audio.")
            return ""
        except sr.RequestError as e:
            print(f"An error occurred during audio recognition: {e}")
            return ""

def on_press(key):
    global recording
    try:
        if key.char == 'r':  # Wenn die 'r'-Taste gedrückt wird
            recording = True
            print("Trigger activated! Recording...")
            user_input = record_user_speech()
            recording = False

            if user_input:
                response = chat_with_ollama(user_input)
                mp3_file = "output2.mp3"

                # Convert text to speech and save as an MP3
                text_to_speech(response, mp3_file)

                # Play the generated MP3
                play_mp3(mp3_file)

                print("Luminara:")
                print(response)

    except AttributeError:
        pass  # Ignoriere andere Tasten als 'r'

def main_loop():
    with keyboard.Listener(on_press=on_press) as listener:
        print("Press 'R' to start recording...")
        listener.join()  # Warten, bis der Listener gestoppt wird

if __name__ == '__main__':
    main_loop()
