import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      // component: () => import('../views/LoginView.vue'),
      component: () => import('@/components/auth/Login.vue'),
    },  
    {
      path: '/register',
      name: 'register',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      // component: () => import('../views/LoginView.vue'),
      component: () => import('@/components/auth/Register.vue'),
    },          
    {
      path: '/documents',
      name: 'documents',
      component: () => import('@/components/Documents.vue'),
    },
    {
      path: '/users',
      name: 'users',
      component: () => import('@/components/Users.vue'),
    },    
    {
      path: '/:catchAll(.*)',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue'),
    },

  ],
})

export default router
