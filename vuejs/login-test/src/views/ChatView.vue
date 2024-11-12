<template>
  <div class="ollama-chat">
    <h2>Ollama Chat</h2>

    <!-- Dark Mode Toggle Button -->
    <button @click="toggleDarkMode" class="dark-mode-toggle">
      {{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}
    </button>

    <!-- Dropdown zur Auswahl des KI-Modells -->
    <div class="model-selection" :class="{ 'dark-mode': isDarkMode }">
      <label for="model">Wähle ein KI-Modell:</label>
      <select v-model="selectedModel" id="model">
        <option value="llama3.2:1b">LLaMA 3.2 - 1B von Meta (Besonders schnell)</option>
        <option value="llama3.2">
          LLaMA 3.2 - 2B von Meta (neuestes Modell, langsamer als 1B)
        </option>
        <option value="gemma2">Gemma2 von Google (langsamer)</option>
        <option value="llama3.1">LLaMA 3.1 von Meta (älter und langsamer)</option>
        <option value="llava:13b">
          LLaVA 13B (am langsamsten, aber mit Vision [Vision wird noch implementiert])
        </option>
        <option value="mario">Per System Prompt soll die AI wie Mario reden</option>
        <option value="htlstudent">
          Ist eine virtuelle Person, die wie eine HTL-Schülerin oder ein HTL-Schüler redet
        </option>
      </select>
    </div>

    <!-- Anzeige der Nachrichten im Chat-Format -->
    <div class="chat-box">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['message', message.type, { 'dark-mode': isDarkMode }]"
      >
        <!-- Benutzer-Nachrichten als einfacher Text -->
        <p v-if="message.type === 'user'">{{ message.text }}</p>
        <!-- Ollama-Nachrichten als formatiertes HTML -->
        <div v-else v-html="message.formattedText"></div>
      </div>
    </div>

    <!-- Eingabefeld und Button -->
    <div class="input-area">
      <input
        v-model="userInput"
        placeholder="Frag Ollama..."
        @keydown.enter="sendMessage"
        class="chat-input"
      />
      <button @click="sendMessage" class="send-button">
        <i class="fas fa-paper-plane"></i> Absenden
      </button>
    </div>

    <div v-if="loading" class="loading">Lädt...</div>
    <div v-if="error" class="error">
      <p>Es gab ein Problem bei der Kommunikation mit Ollama: {{ error }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import Prism from 'prismjs'
import 'prismjs/themes/prism.css' // Für Light Mode
import 'prismjs/themes/prism-okaidia.css' // Für Dark Mode (optional)

export default {
  data() {
    return {
      userInput: '',
      loading: false,
      error: '',
      messages: [], // Hier werden die Nachrichten (Benutzer + Ollama) gespeichert
      selectedModel: 'llama3.2:1b', // Standardmäßig ausgewähltes Modell für Ollama
      isDarkMode: false, // Dark Mode Status
    }
  },
  methods: {
    async sendMessage() {
      if (this.userInput.trim() === '') {
        this.error = 'Prompt darf nicht leer sein!'
        return
      }

      // Füge die Benutzernachricht der Nachrichtenliste hinzu
      this.messages.push({ type: 'user', text: this.userInput })

      this.loading = true
      this.error = ''

      try {
        // Anfrage an Ollama senden
        const url = 'http://localhost:11434/v1/completions' // Anpassen je nach deiner Ollama-API-URL

        // HTTP-POST-Anfrage an Ollama mit dem ausgewählten Modell
        const response = await axios.post(
          url,
          {
            model: this.selectedModel, // Verwendet das ausgewählte Modell
            prompt: this.userInput, // Benutzer-Eingabe
          },
          {
            headers: {
              'Content-Type': 'application/json', // Header für JSON
            },
          },
        )

        // Füge die Antwort von Ollama der Nachrichtenliste hinzu
        const botResponse = response.data.choices
          ? response.data.choices[0].text
          : response.data.error

        // Konvertiere Markdown zu HTML und säubere es
        const rawHtml = marked(botResponse)
        const cleanHtml = DOMPurify.sanitize(rawHtml)

        // Erstelle ein temporäres Element, um Prism auf das HTML anzuwenden
        const tempDiv = document.createElement('div')
        tempDiv.innerHTML = cleanHtml
        Prism.highlightAllUnder(tempDiv)

        // Füge die formatierten und hervorgehobenen HTML-Inhalte hinzu
        this.messages.push({ type: 'ollama', text: botResponse, formattedText: tempDiv.innerHTML })
      } catch (err) {
        this.error = `Fehler: ${err.message}`
      } finally {
        this.loading = false
        this.userInput = '' // Eingabefeld zurücksetzen
        this.$nextTick(() => {
          // Nach dem Update des DOMs Prism Highlighting anwenden
          Prism.highlightAll()
          this.addCopyButtons()
        })
      }
    },
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode
      document.body.classList.toggle('dark-mode', this.isDarkMode)
      document.querySelector('.ollama-chat').classList.toggle('dark-mode', this.isDarkMode)

      // Dynamisch das Prism.js Theme wechseln
      const prismLink = document.getElementById('prism-theme')
      if (prismLink) {
        prismLink.href = this.isDarkMode
          ? 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-okaidia.min.css'
          : 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css'
      } else {
        const link = document.createElement('link')
        link.id = 'prism-theme'
        link.rel = 'stylesheet'
        link.href = this.isDarkMode
          ? 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-okaidia.min.css'
          : 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css'
        document.head.appendChild(link)
      }
    },
    addCopyButtons() {
      // Finde alle <pre> Elemente innerhalb der Chat-Nachrichten
      const codeBlocks = this.$el.querySelectorAll('.message.ollama pre')

      codeBlocks.forEach((block) => {
        // Vermeide das Hinzufügen mehrerer Buttons
        if (!block.querySelector('.copy-button')) {
          const button = document.createElement('button')
          button.innerText = 'Kopieren'
          button.className = 'copy-button'
          button.addEventListener('click', () => {
            const code = block.querySelector('code').innerText
            navigator.clipboard
              .writeText(code)
              .then(() => {
                button.innerText = 'Kopiert!'
                setTimeout(() => {
                  button.innerText = 'Kopieren'
                }, 2000)
              })
              .catch(() => {
                button.innerText = 'Fehler!'
                setTimeout(() => {
                  button.innerText = 'Kopieren'
                }, 2000)
              })
          })
          block.appendChild(button)
        }
      })
    },
  },
}
</script>

<style scoped>
/* Grundlegende Stile für die Chat-Komponente */
.ollama-chat {
  font-family: 'Roboto', sans-serif;
  margin: 20px auto;
  padding: 25px;
  border: 1px solid #ced4da; /* Neutrales Grau für Ränder */
  border-radius: 12px;
  max-width: 700px;
  background-color: #f0f4f8; /* Helles Grau für den allgemeinen Hintergrund */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1); /* Leichter Schatten */
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: relative; /* Für den Dark Mode Toggle Button */
}

/* Dark Mode Stile */
.ollama-chat.dark-mode {
  background-color: #1e1e1e; /* Dunkles Grau für den Hintergrund */
  border-color: #444; /* Dunkleres Grau für Ränder */
  box-shadow: 0 4px 20px rgba(255, 255, 255, 0.1); /* Heller Schatten */
}

.dark-mode-toggle {
  position: absolute;
  top: 20px;
  right: 20px;
  background-color: #20c997; /* Lebendiges Türkis */
  color: #fff;
  border: none;
  padding: 10px 15px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.dark-mode-toggle:hover {
  background-color: #1aa179; /* Etwas dunkleres Türkis für Hover */
}

.dark-mode-toggle:active {
  transform: scale(0.98);
}

.dark-mode-toggle.dark-mode {
  background-color: #bb86fc; /* Kräftiges Lila im Dark Mode */
}

.dark-mode-toggle.dark-mode:hover {
  background-color: #985eff; /* Etwas dunkleres Lila für Hover im Dark Mode */
}

/* Überschrift */
.ollama-chat h2 {
  font-size: 1.8rem;
  color: #1e90ff; /* Kräftiges Blau */
  text-align: center;
  margin-bottom: 10px;
}

.ollama-chat.dark-mode h2 {
  color: #bb86fc; /* Kräftiges Lila im Dark Mode */
}

/* Modell-Auswahl */
.model-selection {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.model-selection label {
  font-weight: 500;
  color: #333;
}

.ollama-chat.dark-mode .model-selection label {
  color: #fff;
}

.model-selection select {
  padding: 10px;
  border: 1px solid #ced4da; /* Neutrales Grau für Ränder */
  border-radius: 8px;
  font-size: 1rem;
  background-color: #fff;
  transition: border-color 0.3s;
}

.ollama-chat.dark-mode .model-selection select {
  background-color: #333;
  color: #fff;
  border-color: #1e90ff; /* Kräftiges Blau für Fokus */
}

.model-selection select:focus {
  border-color: #1e90ff; /* Kräftiges Blau für Fokus */
  outline: none;
}

.ollama-chat.dark-mode .model-selection select:focus {
  border-color: #bb86fc; /* Kräftiges Lila für Fokus im Dark Mode */
}

/* Chat-Box */
.chat-box {
  flex: 1;
  max-height: 400px;
  overflow-y: auto;
  padding: 15px;
  background-color: #ffffff; /* Weiß für Chat-Bubbles */
  border-radius: 10px;
  box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.05); /* Leichter innerer Schatten */
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.ollama-chat.dark-mode .chat-box {
  background-color: #2a2f32; /* Dunkleres Grau für Chat-Bubbles im Dark Mode */
  box-shadow: inset 0 2px 8px rgba(255, 255, 255, 0.1); /* Hellerer innerer Schatten */
}

/* Nachrichten */
.message {
  padding: 12px 20px;
  border-radius: 20px;
  max-width: 75%;
  word-wrap: break-word;
  position: relative;
  transition:
    background-color 0.3s,
    transform 0.2s;
}

.message.user {
  align-self: flex-end;
  background-color: #cce5ff; /* Hellblau für Benutzernachrichten */
  color: #004085; /* Dunkles Blau für Text */
}

.ollama-chat.dark-mode .message.user {
  background-color: #3333cc; /* Dunkles Blau für Benutzernachrichten im Dark Mode */
  color: #e0e0e0; /* Helles Grau für Text im Dark Mode */
}

.message.ollama {
  align-self: flex-start;
  background-color: #d4edda; /* Hellgrün für Ollama-Nachrichten */
  color: #155724; /* Dunkles Grün für Text */
  position: relative;
}

.ollama-chat.dark-mode .message.ollama {
  background-color: #228b22; /* Dunkles Grün für Ollama-Nachrichten im Dark Mode */
  color: #f1f1f1; /* Helles Grau für Text im Dark Mode */
}

/* Eingabebereich */
.input-area {
  display: flex;
  gap: 10px;
}

.chat-input {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #ced4da; /* Neutrales Grau für Ränder */
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); /* Leichter Schatten */
  background-color: #fff;
  color: #333;
}

.ollama-chat.dark-mode .chat-input {
  background-color: #333;
  color: #fff;
  border-color: #1e90ff; /* Kräftiges Blau für Fokus */
}

.chat-input:focus {
  border-color: #1e90ff; /* Kräftiges Blau für Fokus */
  outline: none;
}

.ollama-chat.dark-mode .chat-input:focus {
  border-color: #bb86fc; /* Kräftiges Lila für Fokus im Dark Mode */
}

/* Senden-Button */
.send-button {
  display: flex;
  align-items: center;
  gap: 5px;
  background-color: #1e90ff; /* Kräftiges Blau */
  color: #fff;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition:
    background-color 0.3s,
    transform 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Leichter Schatten */
}

.send-button:hover {
  background-color: #1c86ee; /* Etwas dunkleres Blau für Hover */
  transform: translateY(-2px);
}

.send-button:active {
  transform: translateY(0);
}

.ollama-chat.dark-mode .send-button {
  background-color: #bb86fc; /* Kräftiges Lila im Dark Mode */
}

.ollama-chat.dark-mode .send-button:hover {
  background-color: #985eff; /* Etwas dunkleres Lila für Hover im Dark Mode */
}

/* Lade- und Fehleranzeige */
.loading {
  text-align: center;
  font-weight: bold;
  color: #ffc107; /* Warmes Gelb für Ladeanzeigen */
}

.error {
  text-align: center;
  color: #dc3545; /* Auffälliges Rot für Fehler */
  font-weight: bold;
  background-color: #f8d7da; /* Helleres Rot für Fehlerhintergrund */
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #dc3545; /* Auffälliges Rot für Fehler */
}

.ollama-chat.dark-mode .error {
  background-color: #721c24; /* Dunkleres Rot für Fehlerhintergrund im Dark Mode */
  color: #f8d7da; /* Helles Rot für Text im Dark Mode */
  border-color: #f5c6cb; /* Hellere Ränder für Fehler im Dark Mode */
}

/* Responsive Anpassungen */
@media (max-width: 768px) {
  .ollama-chat {
    padding: 20px;
  }

  .chat-box {
    max-height: 300px;
  }

  .send-button {
    padding: 10px 16px;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .ollama-chat {
    padding: 15px;
  }

  .model-selection {
    flex-direction: column;
  }

  .send-button {
    padding: 8px 12px;
    font-size: 0.8rem;
  }

  .chat-input {
    padding: 10px 12px;
  }
}

/* Stile für gerendertes Markdown */
.ollama-chat .chat-box .message.ollama {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.ollama-chat .chat-box .message.ollama h1,
.ollama-chat .chat-box .message.ollama h2,
.ollama-chat .chat-box .message.ollama h3 {
  margin: 10px 0;
  font-weight: bold;
}

.ollama-chat .chat-box .message.ollama p {
  margin: 5px 0;
}

.ollama-chat .chat-box .message.ollama pre {
  position: relative;
  background-color: #f5f5f5;
  padding: 10px;
  border-radius: 5px;
  overflow-x: auto;
}

.ollama-chat.dark-mode .chat-box .message.ollama pre {
  background-color: #444;
  color: #f8f8f2;
}

.ollama-chat .chat-box .message.ollama code {
  background-color: #eaeaea;
  padding: 2px 4px;
  border-radius: 4px;
}

.ollama-chat.dark-mode .chat-box .message.ollama code {
  background-color: #555;
  color: #f8f8f2;
}

.ollama-chat .chat-box .message.ollama a {
  color: #1e90ff;
  text-decoration: none;
}

.ollama-chat.dark-mode .chat-box .message.ollama a {
  color: #bb86fc;
}

.ollama-chat .chat-box .message.ollama a:hover {
  text-decoration: underline;
}

/* Stil für Copy-Button */
.copy-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: rgba(0, 0, 0, 0.5);
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  opacity: 0;
  transition: opacity 0.3s;
}

pre:hover .copy-button {
  opacity: 1;
}

.ollama-chat.dark-mode .copy-button {
  background-color: rgba(255, 255, 255, 0.5);
  color: #000;
}
</style>
