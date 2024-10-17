![GitHub stars](https://img.shields.io/github/stars/Luna-Schaetzle/Diploma-thesis "GitHub stars")
![GitHub license](https://img.shields.io/github/license/Luna-Schaetzle/Diploma-thesis "GitHub license")
![GitHub contributors](https://img.shields.io/github/contributors/Luna-Schaetzle/Diploma-thesis "GitHub contributors")
![GitHub last commit](https://img.shields.io/github/last-commit/Luna-Schaetzle/Diploma-thesis "GitHub last commit")
![GitHub repo size](https://img.shields.io/github/repo-size/Luna-Schaetzle/Diploma-thesis "GitHub repo size")
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Luna-Schaetzle/Diploma-thesis "GitHub code size in bytes")
![GitHub language count](https://img.shields.io/github/languages/count/Luna-Schaetzle/Diploma-thesis "GitHub language count")
![GitHub top language](https://img.shields.io/github/languages/top/Luna-Schaetzle/Diploma-thesis "GitHub top language")
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/Luna-Schaetzle/Diploma-thesis "GitHub commit activity")

# SAIPiA - Self-sufficient Artificial Intelligent Raspberry Pi Assistant

**SAIPiA** (Self-sufficient Artificial Intelligent Raspberry Pi Assistant) ist ein autonomes, intelligentes System, das auf einem Raspberry Pi 5 basiert. Es kombiniert KI-gestützte Funktionen wie Sprachsteuerung, Bildverarbeitung, Datenbankzugriff und maschinelles Lernen, um vielseitige Aufgaben effizient zu bewältigen. Mit einem modularen Aufbau und der flexiblen Erweiterbarkeit liegt der Fokus des Projekts stark auf der Nutzung von Open-Source-Technologien.

## Projektübersicht

SAIPiA ist eine Diplomarbeit, die die folgenden Kernbereiche umfasst:
- Sprach- und Bildverarbeitung
- Integration von KI-Modellen zur Aufgabenerfüllung
- Optimierung von Hardware- und Softwarekomponenten
- Einsatz von Open-Source-Lösungen
- Raspberry Pi als Basis mit Serverunterstützung für erweiterte Rechenlast
- Aufbau eines dedizierten AI-Servers für leistungsintensive Modelle
- Einbindung externer Dienste wie Wetterdaten

## Funktionsumfang

- **Sprachsteuerung und -ausgabe**: Nutzung von OpenAI Whisper für präzisen Sprachinput und Suche nach optimierter Text-to-Speech-Bibliothek für Sprachoutput.
- **Bildgenerierung und Objekterkennung**: Implementierung von KI-Modellen für Edge-Technologie, um lokale Bildverarbeitung zu ermöglichen.
- **KI-Modellintegration**: Einsatz und Benchmarking von LLAMA3.2 sowie Integration serverbasierter Modelle, die auf einem dedizierten AI-Server laufen.
- **Wetterdatenintegration**: Abfrage und Darstellung aktueller Wetterdaten über die API von wttr.in.

## Verwendete Technologien

- **Raspberry Pi 5**
- **Ubuntu-basierter AI-Server** (optional für komplexe Berechnungen)
- **Python 3.x** zur Entwicklung und Integration der Module
- **wttr.in API** zur Wetterintegration
- (Weitere Technologien werden im Projektverlauf ergänzt)

## Detaillierte Funktionen

### LLAMA3.2 Integration
LLAMA3.2 wird zur Textverarbeitung und weiteren AI-Aufgaben genutzt. Zukünftige Erweiterungen beinhalten den Einsatz leistungsstärkerer Modelle (z.B. LLAMA3.2:1b), die serverseitig laufen, um die Rechenleistung des Raspberry Pi zu entlasten.

### Sprachsteuerung
- **Input**: OpenAI Whisper für präzise Spracherkennung.
- **Output**: Ermittlung einer fortgeschrittenen Text-to-Speech-Bibliothek, um natürliche Sprachwiedergabe zu gewährleisten.

### Wetterintegration
- **wttr.in API** wird genutzt, um Wetterinformationen abzufragen und in SAIPiA darzustellen. Optimierungen zur besseren Datenpräsentation sind geplant.

### News-Integration
- **NEWS-API** wird für das Abrufen und Anzeigen aktueller Nachrichten verwendet. Weitere Details zur Umsetzung folgen.

### Bildverarbeitung und -erkennung
- Lokale Verarbeitung von Bilddaten mit KI-Modellen über Edge-Computing, um Echtzeitergebnisse auf dem Raspberry Pi zu erzielen.
- Für komplexere Bildgenerierungen wird ein AI-Server eingesetzt.

## Hardware

Die Hardware-Konfiguration von SAIPiA umfasst:
- **Raspberry Pi 5** als Hauptsystem
- **Kamera** für Objekterkennung und Umgebungserkennung
- **AI Accelerator** zur Beschleunigung der Bild- und Objekterkennung
- **AI-Server** für leistungsintensive KI-Modelle 
- **Weitere Komponenten** in Abstimmung mit Gabriel

## Screenshots & Demos  

[*wird ergänzt*]

## Roadmap

- **Erweiterung der KI-Modelle**: Integration und Optimierung fortgeschrittener KI-Modelle (z.B. LLAMA3.2:1b).
- **Sprachsteuerungsoptimierung**: Verbesserung der Sprachwiedergabe und Suche nach optimierten Bibliotheken.
- **Wetterdatenintegration**: Verbesserung der Darstellung und Nutzung der Wetterinformationen von wttr.in.
- **Hardware-Tests**: Fortlaufende Tests zur Nutzung des Raspberry Pi in Kombination mit der Kamera und dem AI Accelerator.
- **Rechts- und Open-Source-Recherche**: Untersuchung der rechtlichen Rahmenbedingungen und Open-Source-Lizenzen im Rahmen der Diplomarbeit.

## Zukunftspläne

In den kommenden Monaten planen wir:
- Die Integration weiterer externer APIs (z.B. für Verkehrsdaten).
- Erweiterungen durch Objekterkennung für spezifische Anwendungsfälle wie Smart Home (eventuell).
- Optimierung der Sprachsteuerung mit mehrsprachiger Unterstützung.

## Lizenzierung

Das Projekt verwendet die GNU General Public License v3.0 (GPL-3.0) für die Software und die Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0) für die Dokumentation.
