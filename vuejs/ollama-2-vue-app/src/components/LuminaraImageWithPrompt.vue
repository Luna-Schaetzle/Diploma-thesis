<template>
    <div class="luminara-image-prompt">
      <h1>Bild hochladen und an Ollama schicken</h1>
  
      <!-- Eingabefeld für den Prompt -->
      <div class="input-area">
        <input
          v-model="userInput"
          placeholder="Gib einen Prompt ein..."
          @keydown.enter="sendRequest"
          class="prompt-input"
        />
      </div>
  
      <!-- Bild hochladen -->
      <div class="upload-area">
        <label for="image-upload">Bild auswählen:</label>
        <input type="file" id="image-upload" @change="handleImageUpload" />
      </div>
  
      <!-- Button zum Absenden -->
      <div class="button-area">
        <button @click="sendRequest" class="send-button">
          Anfrage senden
        </button>
      </div>
  
      <!-- Anzeige, wenn das Bild und der Prompt gesendet werden -->
      <div v-if="loading" class="loading">Anfrage wird gesendet...</div>
      <div v-if="error" class="error">{{ error }}</div>
  
      <!-- Anzeige der Antwort von Ollama -->
      <div v-if="ollamaResponse">
        <h3>Ollama Antwort:</h3>
        <p>{{ ollamaResponse }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        userInput: "", // Text-Prompt des Benutzers
        imageBase64: "", // Base64-kodiertes Bild
        loading: false,
        error: "",
        ollamaResponse: null, // Antwort von Ollama
      };
    },
    methods: {
      // Methode zum Hochladen und Base64-Kodieren des Bildes
      handleImageUpload(event) {
        const file = event.target.files[0];
        const reader = new FileReader();
  
        reader.onload = () => {
          this.imageBase64 = reader.result.split(",")[1]; // Nur den Base64-Teil extrahieren
        };
  
        if (file) {
          reader.readAsDataURL(file); // Bild in Base64 kodieren
        }
      },
  
      // Methode zum Senden des Bildes und des Prompts an Flask
      async sendRequest() {
        if (this.userInput.trim() === "" || this.imageBase64 === "") {
          this.error = "Prompt und Bild dürfen nicht leer sein!";
          return;
        }
  
        this.loading = true;
        this.error = "";
        this.ollamaResponse = null;
  
        try {
          // Anfrage an die Flask-Anwendung senden
          const response = await axios.post("http://10.10.11.11:5000/send_image_prompt", {
            prompt: this.userInput,
            image: this.imageBase64, // Base64-kodiertes Bild wird an Flask gesendet
          });
  
          this.ollamaResponse = response.data.choices
            ? response.data.choices[0].text
            : response.data.error;
        } catch (err) {
          this.error = `Fehler: ${err.message}`;
        } finally {
          this.loading = false;
          this.userInput = ""; // Eingabefeld zurücksetzen
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .luminara-image-prompt {
    text-align: center;
    max-width: 600px;
    margin: 0 auto;
  }
  
  .prompt-input {
    padding: 10px;
    width: calc(100% - 22px);
    margin-top: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .upload-area {
    margin-top: 20px;
  }
  
  .send-button {
    margin-top: 20px;
    padding: 10px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .send-button:hover {
    background-color: #45a049;
  }
  
  .loading {
    font-weight: bold;
    color: #007bff;
  }
  
  .error {
    color: red;
  }
  </style>
  