<template>
  <v-container fluid class="text-center">
    <v-row justify="center" align="center" class="fill-height">
      <v-col cols="12">
        <v-icon size="64" class="mb-4">mdi-account-search</v-icon>
        <h1 class="text-h3 font-weight-light mb-4">RecruiterIQ</h1>
        <p class="text-h6 text-medium-emphasis mb-8">
          Intelligent Recruitment Management System
        </p>
        <v-btn 
          color="primary" 
          size="large" 
          prepend-icon="mdi-login"
          @click="$router.push('/login')"
        >
          Get Started
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// Redirect if already authenticated
onMounted(async () => {
  if (authStore.isAuthenticated) {
    const isValid = await authStore.checkAuth()
    if (isValid) {
      router.push('/home')
    }
  }
})
</script>

