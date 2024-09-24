# Diploma Thesis SAIPiA - Self-sufficient Artificial Intelligent Raspberry Pi Assistant

SAIPiA is a cutting-edge, self-sufficient AI assistant running on the Raspberry Pi 5, designed to operate autonomously. It integrates artificial intelligence with a range of functions such as database access, large language models (LLMs), image recognition, speech recognition, and image generation. SAIPiA is a compact, secure, and efficient system that can function both online and offline, ideal for various applications.

## Features
- **AI Assistant**: Supports natural language understanding and responses powered by LLMs.
- **Speech Recognition**: Converts speech to text for voice commands and interactions.
- **Image Recognition**: Recognizes objects and scenes through camera input.
- **Image Generation**: Generates images based on user input or AI-driven creativity.
- **Offline Functionality**: Works without an internet connection, leveraging local databases and resources.
- **Expandable**: Supports GPIO, USB, and other Raspberry Pi interfaces for project-specific extensions.
- **Energy-Efficient**: Powered by an internal battery, rechargeable via USB-C.

## System Requirements
- Raspberry Pi 5 (or compatible hardware)
- Minimum 8 GB SD card for storage
- Display (Touchscreen or Monitor)
- USB Keyboard and Mouse
- Camera module (for image recognition)
- Microphone (for speech recognition)
- Speaker (for audio output)
- Internet connection (optional, for online functionalities)

## software architecture
- **Operating System**: 
- **Programming Language**: Python 3.x
- **Libraries**: OpenCV, PyTorch, TensorFlow, SpeechRecognition
- **Databases**: SQLite (local), MySQL (optional, for online mode)
- **AI Models**: LLAMA, ...
- **APIs**:  

## Usage

- **Command Line Interface (CLI)**: Interact with SAIPiA using text-based commands.
- **Speech Commands**: SAIPiA listens for voice commands and responds accordingly.
- **Image Recognition**: Capture images using the camera module and have them processed for object detection.
- **Image Generation**: Input text prompts to generate AI-driven images.

## Project Structure
```
SAIPiA/
│
├── data/                     # Local databases and datasets
├── models/                   # Pre-trained models for AI functionality
├── src/                      # Source code for the system
│   ├── ai_assistant.py        # Core logic for AI assistant
│   ├── speech_recognition.py  # Speech-to-text and command parsing
│   ├── image_recognition.py   # Image processing and recognition
│   └── image_generation.py    # AI-driven image generation logic
├── tests/                    # Unit tests for each component
└── README.md                 # Project documentation (this file)
```

## Contributors
- **Project Lead**: Luna Schätzle
- **System Integration**: Florian Prantstetter 
- **Database Management**: Gabriel Mrkonja
- **AI/LLM Specialist**: Luna

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
Special thanks to the open-source community for providing tools and resources that made this project possible.

---

Feel free to modify this according to your project needs and the specific software components involved!


# Planned expentions on the backend AI
- change the models 
- add more models
- voice input 
- voice output (with Python voice libary)
- add more languages
- voice translation
- voice output via ai voice
- moduele expansions
    - Weather database 
    - News database
    - Music database
    - Time 
    - Date 
    - Calendar
    - Reminder
    - Alarm
    - Timer
- user identification (it takes every minute or so a picture of the user and compares it with the database if the user is in the database it will greet the user with the name, if they are not in the database it will ask for the name and add it to the database)

All the databases get updated if SAIPIA gets access to the internet. the database entries get time stampes so the user can see when the last update was.

