import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

// Import the functions you need from the SDKs you need
import { initializeApp } from 'firebase/app'
//import { getAnalytics } from 'firebase/analytics'
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: 'AIzaSyBePcxEC-m_mDmyyJvMIMZXWl1CkGd8EKQ',
  authDomain: 'diploma-thesis-test-acd24.firebaseapp.com',
  projectId: 'diploma-thesis-test-acd24',
  storageBucket: 'diploma-thesis-test-acd24.firebasestorage.app',
  messagingSenderId: '824980751548',
  appId: '1:824980751548:web:7e2e269746ce7391063cb9',
  measurementId: 'G-L39D32Y214',
}

// Initialize Firebase
initializeApp(firebaseConfig)
//const analytics = getAnalytics(app)

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
