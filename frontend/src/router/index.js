/**
 * router/index.ts
 *
 * Automatic routes for `./src/pages/*.vue`
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router'
import { setupLayouts } from 'virtual:generated-layouts'
import { routes } from 'vue-router/auto-routes'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: setupLayouts(routes),
})

// Authentication guard
router.beforeEach(async (to, from, next) => {
  // Import auth store dynamically to avoid circular dependency
  const { useAuthStore } = await import('@/stores/auth')
  const authStore = useAuthStore()

  const requiresAuth = to.matched.some(record => record.name === '/home')
  const isLoginPage = to.path === '/login'

  if (requiresAuth && !authStore.isAuthenticated) {
    // Redirect to login if trying to access protected route without auth
    next('/login')
  } else if (isLoginPage && authStore.isAuthenticated) {
    // Redirect to protected route if already authenticated and trying to access login
    const isValid = await authStore.checkAuth()
    if (isValid) {
      next('/home')
    } else {
      next()
    }
  } else {
    next()
  }
})

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err, to) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (localStorage.getItem('vuetify:dynamic-reload')) {
      console.error('Dynamic import error, reloading page did not fix it', err)
    } else {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    }
  } else {
    console.error(err)
  }
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

export default router
