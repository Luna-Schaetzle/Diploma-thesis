<template>
  <div id="app">
    <h1>Luminara AI experimental v.0.3</h1>
    <!-- Einbindung der OllamaChat-Komponente -->
    <OllamaChat />
  </div>
</template>

<script>
// Importiere die OllamaChat-Komponente
import OllamaChat from './components/ollamaChat.vue';

export default {  
  name: 'App',
  components: {
    OllamaChat, // Komponente registrieren
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
</style>
