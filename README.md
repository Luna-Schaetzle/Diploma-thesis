# SAIPiA - Self-sufficient Artificial Intelligent Raspberry Pi Assistant

**SAIPiA** (Self-sufficient Artificial Intelligent Raspberry Pi Assistant) ist ein autonomes, intelligentes System, das auf einem Raspberry Pi 5 basiert. Es kombiniert KI-gestützte Funktionen wie Sprachsteuerung, Bildverarbeitung, Datenbankzugriff und maschinelles Lernen, um verschiedenste Aufgaben zu bewältigen. Das System ist modular aufgebaut und flexibel erweiterbar, mit einem starken Fokus auf Open-Source-Technologien.

## Projektübersicht

SAIPiA wird als Diplomarbeit entwickelt und umfasst die folgenden Kernbereiche:
- Sprach- und Bildverarbeitung
- Integration von AI-Modellen
- Optimierung von Hardware und Software
- Einsatz von Open-Source-Lösungen
- Nutzung von Raspberry Pi als Basis mit Serverunterstützung
- Aufbau eines AI Servers mit starker Rechenleistung für erweiterte Modelle
- Integration von Wetterdaten und anderen externen Diensten

## Funktionsumfang

- **Sprachsteuerung und -ausgabe**: Verwendung von OpenAI Whisper für den Voice Input und einer verbesserten Bibliothek für den Voice Output.
- **Bildgenerierung und Erkennung**: AI-Modelle für Edge-Technologie, um Bildverarbeitung und -erkennung zu ermöglichen.
- **AI-Modellintegration**: Implementierung und Benchmarking von LLAMA3.2 sowie Erweiterung auf serverbasierte Modelle, die auf Flo's Server laufen.
- **Wetterdatenintegration**: Verwendung von wttr.in zur Abrufung und Darstellung von Wetterdaten.


## Verwendete Technologien

- **Raspberry Pi 5** (oder kompatibles Modell)
- **Server** (optional, für erweiterte AI-Modelle und Verarbeitung)
- **Python 3.x**
- **wttr.in** API für Wetterintegration
- (weitere Technologien werden im Laufe des Projekts hinzugefügt)

## Funktionen und Module (Stand: 15.10.2021)

### LLAMA3.2 Integration
LLAMA3.2 wird verwendet, um Textverarbeitung und andere AI-Aufgaben zu erledigen. Tests und mögliche Erweiterungen mit LLAMA3.2:1b sind geplant. Die Modelle laufen auf dem Server, um die Verarbeitungsgeschwindigkeit zu erhöhen.

### Voice Input und Output
- **Input**: Verwendung von OpenAI Whisper für eine akkurate Spracherkennung. (momentan in Arbeit)
- **Output**: Suche nach einer verbesserten Bibliothek für die Sprachsynthese (Text-to-Speech).

### Wetterintegration
- **wttr.in** wird für das Abrufen und Anzeigen von Wetterinformationen in SAIPiA verwendet. Wir arbeiten an der besseren Darstellung dieser Daten.

### NEWS-Integration
- **NEWS-API** wird für das Abrufen und Anzeigen von Nachrichten in SAIPiA verwendet. (Details in Arbeit)

### Bildgenerierung und -erkennung
- Die Integration von AI-Modellen, die auf Edge-Technologie laufen, ist in Arbeit. Das Ziel ist es, eine effiziente Bildverarbeitung direkt auf dem Gerät durchzuführen.
- Da Bildgenerierung viel Rechenleistung erfordert, wird ein Server für erweiterte Modelle verwendet.

## Hardware

Die Hardware von SAIPiA besteht aus:
- **Raspberry Pi 5** als Kernsystem
- **Webcam** für die Objekterkennung
- **Zusätzliche Hardware-Komponenten** werden im Laufe des Projekts detailliert beschrieben (Details mit Gabi in Arbeit).

## Lizenzen

Das Projekt verwendet die GNU General Public License v3.0 (GPL-3.0) für die Software und die Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0) für die Dokumentation.

## Roadmap

- **Integration neuer AI-Modelle**: Erweiterung der vorhandenen Modelle (LLAMA3.2:1b).
- **Optimierung der Sprachsteuerung**: Verbesserung der Output-Qualität und Suche nach besseren Bibliotheken.
- **Wetterdaten**: Optimierung der Darstellung von Wetterdaten aus wttr.in.
- **Hardware-Tests**: Fortlaufende Tests und Berichte zur Nutzung von AI-Heatern.
- **Patent- und Open-Source-Recherche**: Evaluierung der rechtlichen Möglichkeiten im Rahmen der Diplomarbeit.
