<template>
    <div class="ollama-chat">
      <h1>Chatbot</h1>
      
      <!-- Anzeige der Nachrichten im Chat-Format -->
      <div class="chat-box">
        <div v-for="(message, index) in messages" :key="index" :class="['message', message.type]">
          <p>{{ message.text }}</p>
        </div>
      </div>
      
      <!-- Eingabefeld und Button -->
      <input v-model="userInput" placeholder="Frag Ollama..." @keydown.enter="sendMessage" />
      <button @click="sendMessage">Absenden</button>
  
      <div v-if="loading">Lädt...</div>
      <div v-if="error" class="error">
        <p>Es gab ein Problem bei der Kommunikation mit Ollama: {{ error }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        userInput: '', // Benutzereingabe
        messages: [],   // Liste von Nachrichten (Benutzer und Ollama)
        error: '',      // Fehlernachricht
        loading: false, // Ladeindikator
      };
    },
    methods: {
      async sendMessage() {
        if (this.userInput.trim() === '') {
          return; // Verhindert leere Nachrichten
        }
  
        // Füge Benutzereingabe zur Nachrichtenliste hinzu
        this.messages.push({ type: 'user', text: this.userInput });
  
        this.loading = true; // Zeigt den Ladeindikator an
        this.error = ''; // Löscht vorherige Fehler
  
        try {
          // Ollama API-Endpunkt
          const url = 'http://localhost:11434/v1/completions'; // Anpassen je nach deiner Ollama-API-URL
  
          // HTTP-POST-Anfrage an Ollama
          const response = await axios.post(url, {
            model: 'llama3.2:1b', // Beispiel-Modell (anpassen)
            prompt: this.userInput, // Benutzer-Eingabe
          }, {
            headers: {
              'Content-Type': 'application/json', // Header für JSON
            }
          });
  
          // Überprüfen der Antwort
          if (response.data && response.data.choices && response.data.choices.length > 0) {
            const botResponse = response.data.choices[0].text;
            // Füge die Antwort von Ollama zur Nachrichtenliste hinzu
            this.messages.push({ type: 'ollama', text: botResponse });
          } else {
            this.messages.push({ type: 'ollama', text: 'Fehler: Keine Antwort von Ollama erhalten.' });
          }
        } catch (err) {
          console.error('Fehler:', err);
          this.error = `Fehler bei der Anfrage an Ollama: ${err.message}`;
        } finally {
          this.loading = false; // Ladeindikator ausschalten
        }
  
        // Setze das Eingabefeld zurück
        this.userInput = '';
      },
    },
  };
  </script>
  
  <style scoped>
  .error {
    color: red;
    font-weight: bold;
  }
  
  .ollama-chat {
    font-family: Arial, sans-serif;
    margin: 20px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    max-width: 600px;
    margin: 20px auto;
  }
  
  .chat-box {
    max-height: 400px;
    overflow-y: auto;
    margin-bottom: 20px;
  }
  
  .message {
    margin: 10px 0;
    padding: 10px;
    border-radius: 5px;
  }
  
  .message.user {
    background-color: #f1f1f1;
    text-align: left;
  }
  
  .message.ollama {
    background-color: #e0f7fa;
    text-align: right;
  }
  
  input {
    padding: 10px;
    width: calc(100% - 22px);
    margin-top: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  button {
    margin-top: 10px;
    padding: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
  }
  </style>
  