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
            <!-- Admin Only: Create User Section -->
            <v-row v-if="isAdmin" class="mb-6">
              <v-col cols="12">
                <v-card class="pa-4" variant="outlined" color="primary">
                  <v-card-title class="text-h6 mb-4">
                    <v-icon class="mr-2">mdi-account-plus</v-icon>
                    Create New User (Admin Only)
                  </v-card-title>

                  <v-form @submit.prevent="createUser">
                    <v-row>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="newUser.email"
                          label="Email"
                          type="email"
                          prepend-inner-icon="mdi-email"
                          variant="outlined"
                          required
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" md="6">
                        <v-text-field
                          v-model="newUser.password"
                          label="Password"
                          type="password"
                          prepend-inner-icon="mdi-lock"
                          variant="outlined"
                          required
                        ></v-text-field>
                      </v-col>
                    </v-row>

                    <v-row>
                      <v-col cols="12" md="6">
                        <v-select
                          v-model="newUser.role"
                          label="Role"
                          :items="roleOptions"
                          prepend-inner-icon="mdi-account-cog"
                          variant="outlined"
                          required
                        ></v-select>
                      </v-col>
                    </v-row>

                    <!-- Success/Error Messages -->
                    <v-alert
                      v-if="createUserMessage"
                      :type="createUserSuccess ? 'success' : 'error'"
                      class="mb-4"
                      closable
                      @click:close="createUserMessage = ''"
                    >
                      {{ createUserMessage }}
                    </v-alert>

                    <v-btn
                      type="submit"
                      color="success"
                      :loading="creatingUser"
                      prepend-icon="mdi-account-plus"
                    >
                      Create User
                    </v-btn>
                  </v-form>
                </v-card>
              </v-col>
            </v-row>

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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// Check if current user is admin
const isAdmin = computed(() => {
  return authStore.user?.role === 'admin'
})

// Create user form data
const newUser = ref({
  email: '',
  password: '',
  role: 'recruiter'
})

// Role options for dropdown
const roleOptions = [
  { title: 'Admin', value: 'admin' },
  { title: 'Recruiter', value: 'recruiter' },
  { title: 'Hiring Manager', value: 'hiring_manager' }
]

// Create user state
const creatingUser = ref(false)
const createUserMessage = ref('')
const createUserSuccess = ref(false)

// Create user function
const createUser = async () => {
  // Simple validation
  if (!newUser.value.email || !newUser.value.password) {
    createUserMessage.value = 'Please fill in all fields'
    createUserSuccess.value = false
    return
  }

  creatingUser.value = true
  createUserMessage.value = ''

  try {
    const response = await fetch('http://localhost:8000/create-user', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include', // Include cookies for authentication
      body: JSON.stringify({
        email: newUser.value.email,
        password: newUser.value.password,
        role: newUser.value.role
      })
    })

    if (response.ok) {
      const data = await response.json()
      createUserMessage.value = `User created successfully: ${data.email} (${data.role})`
      createUserSuccess.value = true
      
      // Clear form
      newUser.value = {
        email: '',
        password: '',
        role: 'recruiter'
      }
    } else {
      const error = await response.json()
      createUserMessage.value = error.detail || 'Failed to create user'
      createUserSuccess.value = false
    }
  } catch (error) {
    createUserMessage.value = 'Error creating user. Please try again.'
    createUserSuccess.value = false
  } finally {
    creatingUser.value = false
  }
}

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

