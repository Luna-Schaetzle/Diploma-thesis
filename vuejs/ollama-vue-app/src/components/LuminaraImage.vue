<template>
  <div class="luminara-image">
    <h2>Luminara Bildgenerierung powered by stable-diffusion-2-1-base</h2>

    <div class="input-area">
      <input
        v-model="userInput"
        placeholder="Gib einen Prompt für die Bildgenerierung ein..."
        @keydown.enter="generateImage"
        class="image-input"
      />
      <button @click="generateImage" class="generate-button">
        <i class="fas fa-image"></i> Bild generieren
      </button>
    </div>

    <div v-if="loading" class="loading">Bild wird generiert...</div>
    <div v-if="error" class="error">
      <p>{{ error }}</p>
    </div>

    <div v-if="generatedImage">
      <h3>Generiertes Bild:</h3>
      <img
        :src="generatedImage"
        alt="Generated Image"
        class="generated-image"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      userInput: "", // Eingabe des Benutzers
      loading: false, // Ladeindikator
      error: "", // Fehlernachricht
      generatedImage: null, // URL des generierten Bildes
    };
  },
  methods: {
    async generateImage() {
      if (this.userInput.trim() === "") {
        this.error = "Prompt darf nicht leer sein!";
        return;
      }

      this.loading = true;
      this.error = "";
      this.generatedImage = null;

      try {
        // Anfrage an die Flask-API zur Bildgenerierung
        const response = await axios.post(
          "http://10.10.11.11:5000/generate",
          {
            prompt: this.userInput,
          }
        );

        // Bild anzeigen
        const imageUrl = URL.createObjectURL(
          new Blob([response.data], { type: "image/png" })
        );
        this.generatedImage = imageUrl;
      } catch (err) {
        this.error = `Fehler bei der Bildgenerierung: ${err.message}`;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.luminara-image {
  text-align: center;
}

.input-area {
  margin-bottom: 20px;
}

.image-input {
  padding: 10px;
  width: calc(100% - 22px);
  margin-top: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.generate-button {
  margin-top: 10px;
  padding: 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.generate-button:hover {
  background-color: #45a049;
}

.loading {
  font-weight: bold;
  color: #007bff;
}

.generated-image {
  max-width: 100%;
  height: auto;
  border: 2px solid #ddd;
  margin-top: 20px;
}
</style>
