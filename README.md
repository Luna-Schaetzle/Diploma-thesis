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

**SAIPiA** (Self-sufficient Artificial Intelligent Raspberry Pi Assistant) is an autonomous intelligent system based on a Raspberry Pi 5. It combines AI-powered functionalities like voice control, image processing, database access, and machine learning to efficiently handle versatile tasks. With a modular design and flexible expandability, the project focuses heavily on leveraging open-source technologies.

## Project Overview

SAIPiA is a diploma thesis project that covers the following key areas:
- Voice and image processing
- Integration of AI models for task completion
- Optimization of hardware and software components
- Utilization of open-source solutions
- Raspberry Pi as the core system with server support for heavier computational loads
- Setup of a dedicated AI server for resource-intensive models
- Integration of external services like weather data

## Key Features

- **Voice Control and Output**: Using OpenAI Whisper for precise speech recognition and researching an optimized text-to-speech library for natural speech output.
- **Image Generation and Object Recognition**: Implementing AI models for edge technology to enable local image processing.
- **AI Model Integration**: Utilizing and benchmarking LLAMA3.2, along with server-based models running on a dedicated AI server.
- **Weather Data Integration**: Retrieving and displaying current weather data through the wttr.in API.

## Technologies Used

- **Raspberry Pi 5**
- **Ubuntu-based AI server** (optional for complex computations)
- **Python 3.x** for development and module integration
- **wttr.in API** for weather data integration
- (More technologies will be added as the project progresses)

## Detailed Features

### LLAMA3.2 Integration
LLAMA3.2 is used for text processing and other AI-related tasks. Future enhancements include deploying more powerful models (such as LLAMA3.2:1b) on the server side to offload computation from the Raspberry Pi.

### Voice Control
- **Input**: OpenAI Whisper for accurate speech recognition.
- **Output**: Research is underway to find an advanced text-to-speech library for natural voice output.

### Weather Integration
- The **wttr.in API** is used to fetch weather information, which is displayed by SAIPiA. Further optimizations are planned for better data presentation.

### News Integration
- **NEWS API** will be used to retrieve and display current news updates. Implementation details are forthcoming.

### Image Processing and Recognition
- Local image processing with AI models through edge computing for real-time results on the Raspberry Pi.
- More complex image generation will be handled by the AI server.

## Hardware

The SAIPiA hardware configuration includes:
- **Raspberry Pi 5** as the core system
- **Camera** for object and environment recognition
- **AI Accelerator** to boost image and object recognition processing
- **AI Server** for intensive AI model computation
- **Additional components** in collaboration with Gabriel

## Screenshots & Demos

[*To be added*]

## Roadmap

- **AI Model Expansion**: Integration and optimization of advanced AI models (e.g., LLAMA3.2:1b).
- **Voice Control Optimization**: Improving speech output and researching optimized libraries.
- **Weather Data Integration**: Enhancing the display and usage of weather information from wttr.in.
- **Hardware Testing**: Ongoing tests of the Raspberry Pi in combination with the camera and AI accelerator.
- **Legal and Open-Source Research**: Investigating legal frameworks and open-source licenses as part of the diploma thesis.

## Future Plans

In the coming months, we plan to:
- Integrate more external APIs (e.g., for traffic data).
- Explore object recognition extensions for specific use cases like smart home applications (potentially).
- Optimize voice control with multilingual support.

## Licensing

The project is licensed under the GNU General Public License v3.0 (GPL-3.0) for the software and the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0) for the documentation.

