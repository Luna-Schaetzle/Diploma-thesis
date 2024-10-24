<template>
  <div id="app">
    <h1>Bildgenerierungsprogramm mit Stable Diffusion</h1>
    <input v-model="prompt" placeholder="Bitte geben Sie Ihren Prompt ein" />
    <button @click="generateImage">Bild generieren</button>
    <div v-if="message">{{ message }}</div>

    <h2>Galerie der generierten Bilder</h2>
    <div class="gallery">
      <div v-for="image in images" :key="image" class="image-item">
        <img :src="`http://localhost:5000/images/${image}`" :alt="image" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      prompt: '',
      message: '',
      images: []
    };
  },
  methods: {
    async generateImage() {
      this.message = '';
      if (!this.prompt) {
        this.message = 'Fehler: Der Prompt darf nicht leer sein!';
        return;
      }

      try {
        const response = await fetch('http://localhost:5000/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ prompt: this.prompt })
        });

        const data = await response.json();
        if (response.ok) {
          this.message = data.message;
          this.loadImages(); // Lade die Galerie neu
        } else {
          this.message = data.error;
        }
      } catch (error) {
        this.message = 'Ein Fehler ist aufgetreten!';
      }
    },
    async loadImages() {
      try {
        const response = await fetch('http://localhost:5000/images');
        if (response.ok) {
          this.images = await response.json();
        }
      } catch (error) {
        console.error('Fehler beim Laden der Bilder:', error);
      }
    }
  },
  mounted() {
    this.loadImages(); // Lade Bilder beim Start
  }
};
</script>

<style scoped>
#app {
  text-align: center;
}

.gallery {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 20px;
}

.image-item {
  margin: 10px;
}

.image-item img {
  max-width: 200px;
  height: auto;
  border: 1px solid #ccc;
  border-radius: 8px;
}
</style>
