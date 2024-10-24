import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import ImageGallery from '../components/ImageGallery.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/gallery',
    name: 'Gallery',
    component: ImageGallery
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
