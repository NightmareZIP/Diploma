// Подключение компонентов
import { createRouter, createWebHistory } from 'vue-router'
import Register from '../views/Register.vue'
import CompanyRegister from '../views/CompanyRegister.vue'
import HomeView from '../views/HomeView.vue'
import Login from '../views/Login.vue'
import Calendar from '../views/Calendar.vue'
import Profile from '../views/Profile.vue'
import CompanyInfo from '../views/CompanyInfo.vue'
import Workers from '../views/Workers.vue'

// Объявление объекта роутера
const routes = [
  {
    path: '/', //Задаем путь подлкючения
    name: 'home', //Задаем имя, для возможности простого поиска данной настрйоки 
    component: HomeView, //Задаем название компонента, который необходимо подключить
    meta: { requiresAuth: false }, // Помечаем, что для посещения страницы не нужна авторизация

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
    meta: { requiresAuth: true },

    component: Calendar
  },

  {
    path: '/my-calendar/:id',
    name: 'my-calendar-id',
    meta: { requiresAuth: true },
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
    meta: { requiresAuth: true },

    component: Profile
  },

  {
    path: '/company-info',
    name: 'company-info',
    meta: { requiresAuth: true },

    component: CompanyInfo
  },
  {
    path: '/workers',
    name: 'workers',
    meta: { requiresAuth: true },

    component: Workers
  },

]

// Создаем объект роутера
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

//Пероверка, требуется ли авторизация для просмотра страницы
router.beforeEach((to, from) => {
  if (to.meta.requireLogin && !store.state.isAuthenticated) {
    return {
      path: '/login',
      query: { redirect: to.fullPath },
    }
  }
})
export default router
