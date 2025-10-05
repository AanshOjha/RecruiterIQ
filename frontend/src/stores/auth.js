import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // Simple state - no token needed (it's in httpOnly cookie)
  const user = ref(null)
  const loading = ref(false)
  const isAuthenticated = ref(false)

  // Simple login function
  const login = async (email, password) => {
    loading.value = true
    try {
      const response = await fetch('http://localhost:8000/login', {
        method: 'POST',
        credentials: 'include', // ← Include cookies
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Login failed')
      }

      const data = await response.json()
      
      // Set user info (token is in httpOnly cookie automatically)
      user.value = data.user
      isAuthenticated.value = true

    } catch (error) {
      console.error('Login error:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // Simple logout function
  const logout = async () => {
    try {
      await fetch('http://localhost:8000/logout', {
        method: 'POST',
        credentials: 'include'
      })
    } catch (error) {
      console.error('Logout error:', error)
    }
    
    // Clear user data
    user.value = null
    isAuthenticated.value = false
  }

  // Simple auth check function
  const checkAuth = async () => {
    try {
      const response = await fetch('http://localhost:8000/protected', {
        credentials: 'include' // ← Include cookies
      })
      
      if (response.ok) {
        isAuthenticated.value = true
        return true
      } else {
        isAuthenticated.value = false
        return false
      }
    } catch (error) {
      isAuthenticated.value = false
      return false
    }
  }

  return {
    user,
    loading,
    isAuthenticated,
    login,
    logout,
    checkAuth,
  }
})