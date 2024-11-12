<template>
  <div>
    <h1>Create an account</h1>
    <input type="text" placeholder="email" v-model="email" />
    <input type="password" placeholder="Password" v-model="password" />
    <button @click="register">Register</button>
    <button @click="signInWithGoogle">Sign in with Google</button>
  </div>
</template>

<script tab="script" lang="ts">
import { ref } from 'vue'
import {
  getAuth,
  createUserWithEmailAndPassword,
  GithubAuthProvider,
  signInWithPopup,
} from 'firebase/auth'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const router = useRouter()
    const email = ref('')
    const password = ref('')

    const register = () => {
      createUserWithEmailAndPassword(getAuth(), email.value, password.value)
        .then((data) => {
          console.log('User registered', data)
          router.push({ name: 'Chat' })
        })
        .catch((error) => {
          const errorCode = error.code
          const errorMessage = error.message
          console.error('Error registering user', errorCode, errorMessage)
        })
    }

    const signInWithGoogle = () => {
      const provider = new GithubAuthProvider()
      signInWithPopup(getAuth(), provider)
        .then((result) => {
          console.log('User signed in with Google', result)
          router.push({ name: 'Chat' })
        })
        .catch((error) => {
          const errorCode = error.code
          const errorMessage = error.message
          console.error('Error signing in with Google', errorCode, errorMessage)
        })
    }

    return {
      email,
      password,
      register,
      signInWithGoogle,
    }
  },
}
</script>
