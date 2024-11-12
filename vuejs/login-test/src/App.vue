<template>
  <nav>
    <RouterLink to="/">Home</RouterLink>
    <RouterLink to="/about">About</RouterLink>
    <RouterLink to="/Register">Register</RouterLink>
    <RouterLink to="/Chat">Chat</RouterLink>
    <RouterLink to="/Login">Login </RouterLink>
    <button @click="signOutHandel" v-if="isLoggedIn">Sign out</button>
  </nav>
  <RouterView />
</template>

<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { getAuth, onAuthStateChanged, signOut } from 'firebase/auth'
import { ref } from 'vue'
import { onMounted } from 'vue'
import router from './router'

const isLoggedIn = ref(false)

onMounted(() => {
  const auth = getAuth()
  onAuthStateChanged(auth, (user) => {
    if (user) {
      isLoggedIn.value = true
    } else {
      isLoggedIn.value = false
    }
  })
})

const signOutHandel = () => {
  signOut(getAuth())
    .then(() => {
      router.push({ name: 'Home' })
    })
    .catch((error) => {
      console.error('Error signing out', error)
    })
}
</script>
