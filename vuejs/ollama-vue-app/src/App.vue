<template>
  <div id="app">
    <h1>Luminara AI experimental v.0.3</h1>

    <!-- Navigation zum Wechseln zwischen Chat, Bildgenerierung und Galerie -->
    <nav>
      <button @click="activeComponent = 'LuminaraOllama'" :class="{ active: activeComponent === 'LuminaraOllama' }">
        Chat mit Ollama über Flask-API
      </button>
      <button @click="activeComponent = 'OllamaChat'" :class="{ active: activeComponent === 'OllamaChat' }">
        Chat
      </button>
      <!--button @click="activeComponent = 'LuminaraImageWithPrompt'" :class="{ active: activeComponent === 'LuminaraImageWithPrompt' }">
        Bild hochladen und an Ollama schicken
      </button-->
      <button @click="activeComponent = 'LuminaraImage'" :class="{ active: activeComponent === 'LuminaraImage' }">
        Bildgenerierung
      </button>
      <button @click="activeComponent = 'LuminaraGallery'" :class="{ active: activeComponent === 'LuminaraGallery' }">
        Galerie
      </button>

    </nav>

    <!-- Anzeige der aktiven Komponente -->
    <component :is="activeComponent"></component>
  </div>
</template>

<script>
// Importiere die Komponenten
import OllamaChat from './components/OllamaChat.vue';
import LuminaraImage from './components/LuminaraImage.vue';
import LuminaraGallery from './components/LuminaraGallery.vue';
import LuminaraOllama from './components/LuminaraOllama.vue';
import LuminaraImageWithPrompt from './components/LuminaraImageWithPrompt.vue';


export default {
  name: 'App',
  components: {
    OllamaChat,
    LuminaraImage,
    LuminaraGallery,
    LuminaraOllama,
    LuminaraImageWithPrompt,
  },
  data() {
    return {
      activeComponent: 'LuminaraOllama', // Standardmäßig Chat anzeigen
    };
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

nav {
  margin-bottom: 20px;
}

nav button {
  padding: 10px 20px;
  margin: 0 10px;
  cursor: pointer;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
}

nav button.active {
  background-color: #45a049;
}
</style>
