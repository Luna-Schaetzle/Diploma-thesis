<template>
    <div>
      <h1>Bildgenerierung</h1>
      <form @submit.prevent="generateImage">
        <label for="prompt">Bitte geben Sie Ihren Prompt ein:</label><br>
        <input type="text" id="prompt" v-model="prompt" required><br>
        <input type="submit" value="Bild generieren">
      </form>
  
      <div v-if="imageUrl">
        <h2>Generiertes Bild</h2>
        <img :src="imageUrl" alt="Generiertes Bild" />
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        prompt: '',
        imageUrl: ''
      };
    },
    methods: {
      async generateImage() {
        try {
          const response = await axios.post('http://localhost:5000/generate', {
            prompt: this.prompt
          });
          this.imageUrl = `http://localhost:5000/generated_images/${response.data.filename}`;
        } catch (error) {
          console.error('Fehler bei der Bildgenerierung:', error);
        }
      }
    }
  };
  </script>
  