<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <v-card class="pa-6" elevation="2" rounded="lg">
          <v-card-title class="d-flex align-center justify-space-between">
            <div>
              <h1 class="text-h4 font-weight-light">Dashboard</h1>
              <p class="text-subtitle-1 text-medium-emphasis mt-2">
                Welcome to RecruiterIQ, {{ authStore.user?.email }}
                <br>
                Role: {{ authStore.user?.role || 'N/A' }}
              </p>
            </div>
            <v-btn
              color="primary"
              variant="outlined"
              prepend-icon="mdi-logout"
              @click="handleLogout"
            >
              Logout
            </v-btn>
          </v-card-title>

          <v-card-text class="mt-6">

            <v-row class="mt-6">
              <v-col cols="12">
                <v-card class="pa-4" variant="outlined">
                  <v-card-title class="text-h6 mb-4">
                    <v-icon class="mr-2">mdi-information</v-icon>
                    Protected Route Info
                  </v-card-title>
                  <p class="text-body-1">
                    This is a protected route that requires authentication. 
                    You successfully logged in and can access this content.
                  </p>
                  <v-chip class="mt-2" color="success" variant="outlined">
                    <v-icon start>mdi-shield-check</v-icon>
                    Authenticated
                  </v-chip>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
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

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

// Check authentication on mount
onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }

  const isValid = await authStore.checkAuth()
  if (!isValid) {
    router.push('/login')
  }
})
</script>

