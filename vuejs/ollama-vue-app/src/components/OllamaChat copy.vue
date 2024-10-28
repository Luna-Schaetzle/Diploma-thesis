<template>
  <div class="ollama-chat">
    <h2>powered by Ollama</h2>

    <!-- Dropdown zur Auswahl des KI-Modells -->
    <div class="model-selection">
      <label for="model">Wähle ein KI-Modell:</label>
      <select v-model="selectedModel" id="model">
        <option value="llama3.2:1b">LLaMA 3.2 - 1B von Meta (Besonders schnell)</option>
        <option value="llama3.2">LLaMA 3.2 - 2b von Meta (neuestes Modell langsamer als 1B)</option>
        <option value="gemma2">gemma2 von Google (langsamer)</option>
        <option value="llama3.1">LLaMA 3.1 von Meta (älter und langsamer)</option>
        <option value="llava:13b">LLaVA 13B (am langsamsten aber mit vision [Vision wird noch implementiert])</option>
      </select>
    </div>

    <!-- Anzeige der Nachrichten im Chat-Format -->
    <div class="chat-box">
      <div v-for="(message, index) in messages" :key="index" :class="['message', message.type]">
        <p>{{ message.text }}</p>
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
import axios from "axios";

export default {
  data() {
    return {
      userInput: "", // Benutzereingabe
      messages: [], // Liste von Nachrichten (Benutzer und Ollama)
      selectedModel: "llama3.2:1b", // Standardmäßig ausgewähltes Modell
      error: "", // Fehlernachricht
      loading: false, // Ladeindikator
    };
  },
  methods: {
    async sendMessage() {
      if (this.userInput.trim() === "") {
        return; // Verhindert leere Nachrichten
      }

      // Füge Benutzereingabe zur Nachrichtenliste hinzu
      this.messages.push({ type: "user", text: this.userInput });

      this.loading = true; // Zeigt den Ladeindikator an
      this.error = ""; // Löscht vorherige Fehler

      try {
        // Ollama API-Endpunkt
        const url = "http://localhost:11434/v1/completions"; // Anpassen je nach deiner Ollama-API-URL

        // HTTP-POST-Anfrage an Ollama mit dem ausgewählten Modell
        const response = await axios.post(
          url,
          {
            model: this.selectedModel, // Verwendet das ausgewählte Modell
            prompt: this.userInput, // Benutzer-Eingabe
          },
          {
            headers: {
              "Content-Type": "application/json", // Header für JSON
            }
          }
        );

        // Überprüfen der Antwort
        if (response.data && response.data.choices && response.data.choices.length > 0) {
          const botResponse = response.data.choices[0].text;
          // Füge die Antwort von Ollama zur Nachrichtenliste hinzu
          this.messages.push({ type: "ollama", text: botResponse });
        } else {
          this.messages.push({ type: "ollama", text: "Fehler: Keine Antwort von Ollama erhalten." });
        }
      } catch (err) {
        console.error("Fehler:", err);
        this.error = `Fehler bei der Anfrage an Ollama: ${err.message}`;
      } finally {
        this.loading = false; // Ladeindikator ausschalten
      }

      // Setze das Eingabefeld zurück
      this.userInput = "";
    },
  },
};
</script>

<style scoped>
.error {
  color: #ff4d4d;
  font-weight: bold;
}

.ollama-chat {
  font-family: 'Roboto', sans-serif;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  max-width: 600px;
  background-color: #fafafa;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

.model-selection {
  margin-bottom: 20px;
}

.model-selection label {
  font-weight: bold;
  margin-right: 10px;
}

.model-selection select {
  padding: 5px;
  font-size: 16px;
}

.chat-box {
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 20px;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: inset 0px 2px 8px rgba(0, 0, 0, 0.05);
}

.message {
  margin: 10px 0;
  padding: 10px 15px;
  border-radius: 15px;
  max-width: 80%;
  word-wrap: break-word;
}

.message.user {
  background-color: #e0f7fa;
  align-self: flex-start;
}

.message.ollama {
  background-color: #d1c4e9;
  align-self: flex-end;
  text-align: right;
}

.input-area {
  display: flex;
  align-items: center;
}

.chat-input {
  flex: 1;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-right: 10px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

.send-button {
  background-color: #6200ea;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.send-button:hover {
  background-color: #3700b3;
}

.loading {
  text-align: center;
  font-weight: bold;
  color: #007bff;
}
</style>
