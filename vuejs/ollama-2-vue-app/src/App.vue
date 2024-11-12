<template>
  <div id="app" :class="{ 'dark-mode': isDarkMode }">
    <header>
      <h1>Luminara AI v.0.4 (experimental)</h1>
      <!-- Dark Mode Toggle Button -->
      <button @click="toggleDarkMode" class="dark-mode-toggle">
        {{ isDarkMode ? 'Light Mode' : 'Dark Mode' }}
      </button>
    </header>

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
    <div class="component-container">
      <component :is="activeComponent"></component>
    </div>
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
      isDarkMode: false, // Dark Mode Status
    };
  },
  methods: {
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      // Optional: Speichere den Dark Mode Status im Local Storage
      localStorage.setItem('isDarkMode', this.isDarkMode);
    },
  },
  created() {
    // Optional: Lade den Dark Mode Status aus dem Local Storage
    const savedMode = localStorage.getItem('isDarkMode');
    if (savedMode !== null) {
      this.isDarkMode = JSON.parse(savedMode);
    }
  },
};
</script>

<style scoped>
/* Grundlegende Stile für die App */
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f7fa;
  color: #333;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  transition: background-color 0.3s, color 0.3s;
}

/* Dark Mode Stile */
#app.dark-mode {
  background-color: #121212; /* Dunkles Grau für den Hintergrund */
  color: #f0f0f0; /* Helles Grau für den Text */
}

/* Header */
header {
  width: 100%;
  max-width: 800px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

header h1 {
  font-size: 2rem;
  color: #2c3e50;
  transition: color 0.3s;
}

#app.dark-mode header h1 {
  color: #bb86fc; /* Kräftiges Lila im Dark Mode */
}

/* Dark Mode Toggle Button */
.dark-mode-toggle {
  background-color: #20c997; /* Lebendiges Türkis */
  color: #fff;
  border: none;
  padding: 10px 15px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.dark-mode-toggle:hover {
  background-color: #1aa179; /* Etwas dunkleres Türkis für Hover */
}

.dark-mode-toggle:active {
  transform: scale(0.98);
}

#app.dark-mode .dark-mode-toggle {
  background-color: #bb86fc; /* Kräftiges Lila im Dark Mode */
}

#app.dark-mode .dark-mode-toggle:hover {
  background-color: #985eff; /* Etwas dunkleres Lila für Hover im Dark Mode */
}

/* Navigation */
nav {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin-bottom: 30px;
}

nav button {
  padding: 12px 24px;
  background-color: #3498db; /* Kräftiges Blau */
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  transition: background-color 0.3s, transform 0.2s;
  cursor: pointer;
}

nav button:hover {
  background-color: #2980b9; /* Etwas dunkleres Blau für Hover */
  transform: translateY(-2px);
}

nav button.active {
  background-color: #2ecc71; /* Helles Grün für aktiven Button */
}

#app.dark-mode nav button {
  background-color: #1e90ff; /* Kräftiges Blau im Dark Mode */
}

#app.dark-mode nav button.active {
  background-color: #27ae60; /* Dunkleres Grün für aktiven Button im Dark Mode */
}

#app.dark-mode nav button:hover {
  background-color: #1c86ee; /* Etwas dunkleres Blau für Hover im Dark Mode */
}

/* Responsive Anpassungen */
@media (max-width: 600px) {
  nav button {
    flex: 1 1 100%;
    max-width: 300px;
  }
}

/* Komponenten-Anzeige */
.component-container {
  width: 100%;
  max-width: 800px;
  background-color: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s, box-shadow 0.3s;
}

#app.dark-mode .component-container {
  background-color: #1e1e1e; /* Dunkles Grau für den Komponentencontainer im Dark Mode */
  box-shadow: 0 4px 6px rgba(255, 255, 255, 0.1);
}

/* Optional: Übergangseffekte beim Wechseln der Komponenten */
component {
  transition: opacity 0.5s ease-in-out;
}
</style>
