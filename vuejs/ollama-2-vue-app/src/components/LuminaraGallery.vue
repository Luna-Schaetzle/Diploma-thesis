<template>
  <div class="LuminaraGallery">
    <h1>Bildgalerie</h1>
    <div v-if="loading" class="loading">Lade Bilder...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="images.length > 0" class="image-grid">
      <div v-for="(image, index) in images" :key="index" class="image-item" @click="showImage(image)">
        <img :src="`http://10.10.11.11:5000/images/${image}`" :alt="image" />
      </div>
    </div>

    <div v-if="images.length === 0" class="no-images">
      <p>Keine Bilder vorhanden</p>
    </div>

    <!-- Modal zum Anzeigen des großen Bildes -->
    <div v-if="selectedImage" class="modal" @click="closeModal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <img :src="`http://10.10.11.11:5000/images/${selectedImage}`" alt="Selected Image" class="modal-image" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      images: [],         // Liste der Bilder
      loading: false,     // Ladeindikator
      error: null,        // Fehlernachricht
      selectedImage: null // Aktuell ausgewähltes Bild (für die Vergrößerung)
    };
  },
  methods: {
    async fetchImages() {
      this.loading = true;
      this.error = null;

      try {
        const response = await axios.get("http://10.10.11.11:5000/gallery");
        this.images = response.data;
      } catch (err) {
        this.error = `Fehler beim Abrufen der Bilder: ${err.message}`;
      } finally {
        this.loading = false;
      }
    },
    // Methode zum Anzeigen des ausgewählten Bildes im Modal
    showImage(image) {
      this.selectedImage = image;
    },
    // Methode zum Schließen des Modals
    closeModal() {
      this.selectedImage = null;
    }
  },
  created() {
    this.fetchImages(); // Lade Bilder, sobald die Komponente erstellt wurde
  }
};
</script>

<style scoped>
.gallery {
  text-align: center;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
}

.image-item img {
  max-width: 100%;
  height: auto;
  border: 2px solid #ddd;
  cursor: pointer;
  transition: transform 0.2s;
}

.image-item img:hover {
  transform: scale(1.05);
}

.loading, .error, .no-images {
  font-size: 18px;
  margin-top: 20px;
}

/* Modal (Lightbox) Styles */
.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
}

.modal-content {
  position: relative;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  max-width: 90%;
  max-height: 90%;
}

.modal-image {
  max-width: 100%;
  max-height: 100%;
}

.close {
  position: absolute;
  top: 10px;
  right: 20px;
  font-size: 30px;
  font-weight: bold;
  color: #fff;
  cursor: pointer;
}

.close:hover {
  color: #ccc;
}
</style>