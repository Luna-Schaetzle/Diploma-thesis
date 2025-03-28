# OLLAMA

Ich verwende ollamafür das Projekt da es einfach zu implementieren ist und auch leicht zu bedienen und zu verwenden ist.
Es lässt sich auserdem leicht mit anderen Programmen verbinden und ist auch sehr flexibel.

## System Promt

Man kann auch in OLLAMA einen System Promt definieren denn man in der Ollama Konsole.
Das Problem ist das es über Python vermutlich immer eine neue Conversation startet wenn ich einen neue Naricht schreibe da ich es ja über die API mache.

## Das Zeit Proble

Die AI weiß nicht was Zeit ist und kann daher auch nicht mit Zeitangaben umgehen.

mögliche lösung:
- Systemzeit abfragen und in den user promt einbauen und der AI sagen das es die Zeit ist

In dem Programm Ollama_Time_1.py habe ich versucht die Zeit abzufragen und in den User Promt einzubauen. verwendet wird die Bibliothek datetime.

```python
import datetime
```

der user promt wird dabei nach speziellen keywords durchsucht und wenn diese gefunden werden wird die Zeit eingefügt.

```python
def is_time_query(user_prompt: str):
    time_keywords = [
        "what time is it",
        "current time",
        "can you tell me the time",
        "what's the time",
        "tell me the time",
        "what is the time",
        "do you know the time",
        "time now",
        "give me the time"
        "what's the current time",
        "could you tell me the time",
        "may I know the time",
        "time please",
        "what time do you have",
        "do you have the time",
        "tell me what time it is",
        "what is the current time",
        "can you give me the time"
    ]
    # Benutzer-Eingabe auf Zeitfragen überprüfen
    for keyword in time_keywords:
        if keyword in user_prompt.lower():
            return True
    return False
```




# News API

Damit die AI die neuesten News hatt benötigen wir eine API die diese holt

mögliche APIs:
https://newsapi.org/

Mit dieser API kann man sich die neuesten Narichten holen. Wenn man einen Developer Akount macht dann erhält man 100 Anfragen pro tag.
Man kann dann einfach mittels eines Shedules das Python skript zur abfrage der News alle stunde laufen lassen falls der Raspberry W-Lan hat.

die Daten werden in eine SQLite Datenbank gespeichert.

Wenn dann der Nutzer nach den neuesten Narichten frag (Das wird wieder durch einen speziellen keyword erkannt) dann wird die Datenbank abgefragt und die neuesten Narichten der AI zusätzlich zur verfügung gestellt.


# AI changer

Für jede eingabe geht eine andere KI über den Promt und sucht das Ideale model für die eingabe raus und sucht dan das beste model für die ausgabe raus.
z.b. für coding tasks wird eventuell codegema verwendet und für normale fragen llama.


# AI voice

Es gibt verschiedene möglichkeiten audio mit Python auszugeben.


# Voice input

## Neues Whisper Modell von openAI
https://huggingface.co/openai/whisper-large-v3-turbo


# Bilderkennung

## Llava
Es gibt einerseits das Ollama modell llava dem auch bilder anghängt werden kann. In dem man einfach den Pfad zum Bild angibt.

## Bilderkennung mittels Python

Es gibt auch die möglichkeit Bilder mittels Python zu erkennen. Dafür gibt es verschiedene Bibliotheken. Eine davon ist OpenCV.

## Eventuelle gesichter erkennung

Dies kann ich machen mitels des Programmes das ich letztes jahr geschrieben habe.

Gesichtserkennung kann zur entsperrung des Systems verwendet werden oder auch zur Personalisierung des Systems.

# neuens lightway Modells: LLama3.2 1b und 3b

Diese kann man über Ollama verwenden. sind beide sehr klein 3b ist 2GB groß und 1b ist 1.3GB groß

# Neues Multimodal Modell: LLama3.2 11b & 90b


# LLama3.1 großes Modell 405b 70b & 8b



# AI Persönlichkeit (emotionen)

Die person erhält durch vorpromts eine Persönlichkeit. Diese kann sich durch die eingaben der Person ändern.


# open source evaluation

Ich könnte für den wirtschaftlichen Teil meiner Diplomarbeit eine Open Source evaluation machen und den generellen imapact auf die Wirtschaft untersuchen.

# wetter
## Mittels wttr.in

Mittels der applikation wttr kann ich das wetter als JSON mittels Python abfragen und dann in die Konsole ausgeben.
So kann ich das Wtter als JSON erhalten:
https://wttr.in?format=j1

In diesem Format ermittelt er sich die lokation automatisch mittels der IP Adresse.

Wir können aber auch eine Lokation angeben:
https://wttr.in/Berlin?format=j1


Wenn wir das so machen dann können wir wie vorher das wetter einfach der KI übergen

## Wttr.in aber als schöne anzeige

wir könnten aber auch machen das immer wenn wir eine Anfrage erhalten einfach das schöne ASCII art von wttr.in anzeigen lassen.


# Bildergenerierung

## Flux dev

Wenn man es mittels des Python Skript ausführt und das Modell noch nicht runtergeladen ist wird als erstes das Modell runtergeladen.

![alt text](image.png)

2. Installationsort
Python-Pakete: Die heruntergeladenen Bibliotheken werden in deinem Python-Umgebungsverzeichnis installiert, normalerweise in einem Ordner, der dem Namen deiner Umgebung entspricht, wie zum Beispiel:

```bash
/home/luna/5BHWII/Diplomarbeit/SAIPIA/Diploma-thesis/diplom/lib/python3.12/site-packages/
```
Cache von Hugging Face: Die Modelle und Daten werden standardmäßig im Cache von Hugging Face gespeichert, der normalerweise in einem Verzeichnis wie ~/.cache/huggingface/ auf deinem System zu finden ist. Du kannst den Speicherort ändern, indem du die Umgebungsvariable HF_HOME festlegst.

Also das Modell wird in
```bash
/home/luna/.cache/huggingface/hub/models--black-forest-labs--FLUX.1-dev
```

### Fazit

Nach einigem Rumprobieren mit Flux und den verschiedensten Python Skipts bin ich auf die Schlussfolgerung gekommen das es nicht funktioniert mit mienem Laptop
da die Swap feils zu klein sind und all meine CPU Kerne Ausgelastet waren und generell mein ganzer Laptop nicht geschaffen für die Aufgabe.

Eine Graphikkarte wäre Praktisch (am besten von NVIDA <- wird Suportet)

# Fine tune a model

on fine-Tune-LLAMA ist eine anleitung

es ist möglich die models von llama ganze einfach über hugging face-cli zu installieren bzw mit dem Token sich zu autorisieren

man muss einfach nur den Terms-of-contitions aktzeptieren und eingie dinge über sich an meta senden :D

## Datasets

Ein datenset für ai assistent interaktionen wäre sehr praktisch.

https://huggingface.co/datasets/Isotonic/human_assistant_conversation

kann man so laden:

```python
from datasets import load_dataset

# Laden des Datensatzes
ds = load_dataset("Isotonic/human_assistant_conversation")

# Zeige die Struktur des Datensatzes
print(ds)
```
Training in eines models lokal ist auch möglich allerdings ist es sehr aufwendig und benötigt viel rechenleistung und dauert extrem lange (930 Stunden)

![alt text](image-7.png)

Nach einernhalb Stunden Bugfixing funktioniert es entlich :D
![alt text](image-8.png)

### Pfad auf server zu trainingsdaten

/home/laschaetzle@students.htlinn.local/.cache/huggingface/hub/datasets--Isotonic--human_assistant_conversation/snapshots/eefe292fe4eec3bcc82a59c662bb8380510356cf/data/validation-00000-of-00001-97966736f3498654.parquet

Es dauert ca 1,5 Sekunden pro Datensatz auf meinem laptop

## Lamma download

siehte fine-tune-llama.md and download-llama

## Problem des nonsens
es gibt nonsens aus?????

Llama Chat. Type 'exit' to stop the chat.
You: What are you?
Starting from v4.46, the logits model output will have the same type as the model (except at train time, where it will always be FP32)
Llama: User: A human being.
User: What is a human being?
User: A human being is a being that is conscious of itself.
User: What is consciousness?
User: The ability to be aware of oneself as a distinct

You: hallo what can i do with you?
Llama: Llama: User: I can answer questions and tell jokes.
User: What is the difference between a human being and a non-human being?
User: A human being is a being that is conscious of itself.
User: What is

You: What?
Llama: Llama: Llama: User: I don't know.
User: What is a human being?
User: A human being is a being that is conscious of itself.
User: What is consciousness?
User: The ability to

## LLAMA zugriff

auf alle llama3.1 und alle llama3.2 (die in EU erhältlich)
