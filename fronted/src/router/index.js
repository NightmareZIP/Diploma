import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Register from '../views/Register.vue'
import CompanyRegister from '../views/CompanyRegister.vue'

import Login from '../views/Login.vue'
import Calendar from '../views/Calendar.vue'
import Profile from '../views/Profile.vue'
import CompanyInfo from '../views/CompanyInfo.vue'
import Workers from '../views/Workers.vue'


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/register/:companyid',
    name: 'register',
    component: Register
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },

  {
    path: '/my-calendar',
    name: 'my-calendar',

    component: Calendar
  },
  
  {
    path: '/my-calendar/:id',
    name: 'my-calendar-id',

    component: Calendar
  },

  {
    path: '/company-register',
    name: 'company-register',

    component: CompanyRegister
  },

  {
    path: '/profile',
    name: 'profile',

    component: Profile
  },

  {
    path: '/company-info',
    name: 'company-info',

    component: CompanyInfo
  },
  {
    path: '/workers',
    name: 'workers',

    component: Workers
  },
  
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from) => {
  if (to.meta.requireLogin && !store.state.isAuthenticated) {
    return {
      path: '/login',
      // save the location we were at to come back later
      query: { redirect: to.fullPath },
    }
  }
})
export default router
