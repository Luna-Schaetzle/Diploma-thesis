<template>
    <div>
      <h1>Galerie der Bilder</h1>
      <div v-if="images.length">
        <img
          v-for="image in images"
          :key="image"
          :src="`http://localhost:5000/generated_images/${image}`"
          alt="Generiertes Bild"
          style="max-width: 200px; margin: 10px;"
        />
      </div>
      <div v-else>
        <p>Keine Bilder vorhanden.</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        images: []
      };
    },
    async created() {
      await this.fetchImages();
    },
    methods: {
      async fetchImages() {
        try {
          const response = await axios.get('http://localhost:5000/gallery');
          this.images = response.data.images;
        } catch (error) {
          console.error('Fehler beim Abrufen der Bilder:', error);
        }
      }
    }
  };
  </script>
  