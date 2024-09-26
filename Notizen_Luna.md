# OLLAMA

Ich verwende ollama für das Projekt da es einfach zu implementieren ist und auch leicht zu bedienen und zu verwenden ist. 
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