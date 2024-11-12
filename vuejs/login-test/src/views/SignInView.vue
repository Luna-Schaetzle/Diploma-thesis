<template>
  <div>
    <h1>Login</h1>
    <input type="text" placeholder="email" v-model="email" />
    <input type="password" placeholder="Password" v-model="password" />
    <p v-if="errorMessage">{{ errorMessage }}</p>
    <button @click="register">Login</button>
    <button @click="signInWithGoogle">Sign in with Google</button>
  </div>
</template>

<script tab="script" lang="ts">
import { ref } from 'vue'
import {
  getAuth,
  signInWithEmailAndPassword,
  GithubAuthProvider,
  signInWithPopup,
} from 'firebase/auth'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const router = useRouter()
    const email = ref('')
    const password = ref('')
    const errorMessage = ref('')

    const register = () => {
      signInWithEmailAndPassword(getAuth(), email.value, password.value)
        .then((data) => {
          console.log('User registered', data)
          router.push({ name: 'Chat' })
        })
        .catch((error) => {
          const errorCode = error.code
          const errorMessage = error.message
          console.error('Error registering user', errorCode, errorMessage)
          switch (errorCode) {
            case 'auth/invalid-email':
              errorMessage.value = 'Invalid email'
              break
            case 'auth/user-not-found':
              errorMessage.value = 'User not found'
              break
            case 'auth/wrong-password':
              errorMessage.value = 'Wrong password'
              break
            default:
              errorMessage.value = 'Error registering user'
              break
          }
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
      errorMessage,
    }
  },
}
</script>
