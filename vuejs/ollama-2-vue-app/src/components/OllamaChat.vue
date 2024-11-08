<template>
  <div class="ollama-chat">
    <h2>powered by Ollama and Flask-API</h2>

    <!-- Dropdown zur Auswahl des KI-Modells -->
    <div class="model-selection">
      <label for="model">Wähle ein KI-Modell:</label>
      <select v-model="selectedModel" id="model">
        <option value="llava:13b">LLaVA 13B (mit Vision)</option>
        <option value="llama3.2:1b">LLaMA 3.2 - 1B von Meta (Besonders schnell)</option>
        <option value="llama3.2">LLaMA 3.2 - 2B von Meta (neuestes Modell, langsamer als 1B)</option>
        <option value="gemma2">Gemma2 von Google (langsamer)</option>
        <option value="llama3.1">LLaMA 3.1 von Meta (älter und langsamer)</option>
      </select>
    </div>

    <!-- Anzeige der Nachrichten im Chat-Format -->
    <div class="chat-box">
      <div v-for="(message, index) in messages" :key="index" :class="['message', message.type]">
        <p v-if="message.text">{{ message.text }}</p>
        <img v-if="message.image" :src="message.image" alt="User Image" class="chat-image" />
      </div>
    </div>

    <!-- Eingabefeld, Bild-Upload und Button -->
    <div class="input-area">
      <input
        v-model="userInput"
        placeholder="Frag Ollama..."
        @keydown.enter="sendMessage"
        class="chat-input"
      />
      <input type="file" @change="handleImageUpload" accept="image/*" class="image-input" />
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
      userInput: "",
      selectedImage: null, // Für das ausgewählte Bild
      loading: false,
      error: "",
      messages: [], // Hier werden die Nachrichten (Benutzer + Ollama) gespeichert
      selectedModel: "llava" // Standardmäßig ausgewähltes Modell für Ollama
    };
  },
  methods: {
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const base64String = e.target.result.split(',')[1]; // Base64-String ohne Präfix
          this.selectedImage = base64String;
          console.log("Bild erfolgreich konvertiert zu Base64:", base64String.substring(0, 30) + '...'); // Logging
        };
        reader.readAsDataURL(file);
      } else {
        this.error = "Bitte ein gültiges Bild auswählen.";
      }
    },
    async sendMessage() {
      if (this.userInput.trim() === "" && !this.selectedImage) {
        this.error = "Prompt oder Bild muss angegeben sein!";
        return;
      }

      // Füge die Benutzernachricht der Nachrichtenliste hinzu
      if (this.userInput.trim() !== "") {
        this.messages.push({ type: "user", text: this.userInput });
      }
      if (this.selectedImage) {
        const imageUrl = `data:image/*;base64,${this.selectedImage}`;
        this.messages.push({ type: "user", image: imageUrl });
      }

      this.loading = true;
      this.error = "";

      try {
        // Erstelle das JSON-Payload
        const payload = {
          prompt: this.userInput,
          model: this.selectedModel,
        };
        if (this.selectedImage) {
          payload.images = [this.selectedImage];
        }

        console.log("Sende Payload an Backend:", payload); // Logging

        // Anfrage an Flask senden
        const response = await axios.post("http://10.10.11.11:5000/ask_ollama", payload, {
          headers: {
            "Content-Type": "application/json",
          },
        });

        console.log("Antwort vom Backend:", response.data); // Logging

        // Verarbeite die Antwort von Ollama
        if (response.data.error) {
          this.error = response.data.error;
        } else {
          const botResponse = response.data.choices ? response.data.choices[0].text : "Keine Antwort erhalten.";
          this.messages.push({ type: "ollama", text: botResponse });

          // Optional: Wenn das Backend ein generiertes Bild zurückgibt
          if (response.data.generated_image_url) {
            this.messages.push({ type: "ollama", image: response.data.generated_image_url });
          }
        }
      } catch (err) {
        console.error("Fehler beim Senden der Nachricht:", err); // Logging
        this.error = `Fehler: ${err.response?.data?.error || err.message}`;
      } finally {
        this.loading = false;
        this.userInput = ""; // Eingabefeld zurücksetzen
        this.selectedImage = null; // Bild-Input zurücksetzen
      }
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

.chat-image {
  max-width: 100%;
  border-radius: 10px;
  margin-top: 10px;
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

.image-input {
  margin-right: 10px;
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
