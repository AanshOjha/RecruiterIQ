<template>
  <v-container fluid class="fill-height">
    <v-row justify="center" align="center" class="fill-height">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card class="elevation-12">
          <v-card-title class="text-center pa-6">
            <v-icon size="48" class="mb-4">mdi-account-circle</v-icon>
            <h2 class="text-h4 font-weight-light">Login</h2>
            <p class="text-subtitle-1 text-medium-emphasis">Sign in to RecruiterIQ</p>
          </v-card-title>

          <v-card-text class="pa-6">
            <!-- Login Form -->
            <v-form @submit.prevent="handleLogin">
              <!-- Email Input -->
              <v-text-field
                v-model="email"
                label="Email"
                type="email"
                prepend-inner-icon="mdi-email"
                variant="outlined"
                class="mb-4"
                required
              ></v-text-field>

              <!-- Password Input -->
              <v-text-field
                v-model="password"
                label="Password"
                :type="showPassword ? 'text' : 'password'"
                prepend-inner-icon="mdi-lock"
                :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append-inner="showPassword = !showPassword"
                variant="outlined"
                class="mb-4"
                required
              ></v-text-field>

              <!-- Error Message -->
              <v-alert
                v-if="errorMessage"
                type="error"
                class="mb-4"
                closable
                @click:close="errorMessage = ''"
              >
                {{ errorMessage }}
              </v-alert>

              <!-- Login Button -->
              <v-btn
                type="submit"
                color="primary"
                size="large"
                block
                :loading="loading"
                class="mb-4"
              >
                Sign In
              </v-btn>

              <!-- Back to Home Link -->
              <div class="text-center">
                <v-btn
                  variant="text"
                  color="primary"
                  @click="goHome"
                >
                  <v-icon start>mdi-arrow-left</v-icon>
                  Back to Home
                </v-btn>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'LoginPage',
  setup() {
    // Get router and auth store
    const router = useRouter()
    const authStore = useAuthStore()

    // Form data
    const email = ref('')
    const password = ref('')
    const showPassword = ref(false)

    // Error handling
    const errorMessage = ref('')

    // Loading state
    const loading = ref(false)

    // Handle login form submission
    const handleLogin = async () => {
      // Simple validation
      if (!email.value || !password.value) {
        errorMessage.value = 'Please fill in all fields'
        return
      }

      loading.value = true
      errorMessage.value = ''

      try {
        // Call login from auth store
        await authStore.login(email.value, password.value)
        
        // If successful, redirect to protected page
        router.push('/home')
        
      } catch (error) {
        // Show error message
        errorMessage.value = error.message || 'Login failed. Please try again.'
      } finally {
        loading.value = false
      }
    }

    // Go back to home page
    const goHome = () => {
      router.push('/')
    }

    // Return all reactive data and methods
    return {
      email,
      password,
      showPassword,
      errorMessage,
      loading,
      handleLogin,
      goHome
    }
  }
}
</script>

