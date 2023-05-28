<template>
  <!-- Выводим элементы навигации роутера, так же проверяем, аторизован ли пользователь для отобра
  жения каждого из элементов -->
  <nav>
    <router-link to="/">Главная страница|</router-link>
    <router-link to="/my-calendar" v-if=$store.state.isAuthenticated>Мой календарь|</router-link>
    <router-link to="/company-register" v-if=!$store.state.isAuthenticated>Зарегестрировать компанию|</router-link>

    <router-link to="/register/1" v-if=!$store.state.isAuthenticated>Зарегестрироваться|</router-link>
    <router-link to="/login" v-if=!$store.state.isAuthenticated>Авторизоваться|</router-link>
    <router-link to="/profile" v-if=$store.state.isAuthenticated>{{ this.$store.state.user.username }}|</router-link>
    <router-link to="/company-info" v-if=$store.state.isAuthenticated>Данные компании|</router-link>
    <router-link to="/workers" v-if=$store.state.isAuthenticated>Ваши коллеги|</router-link>

    <router-link id='logout' @click="logout" to='' v-if=$store.state.isAuthenticated>Выйти|</router-link>

  </nav>
  <router-view />
</template>

<script>
import axios from 'axios'
// Прописываем информаию о комопненте и логику его работы
export default {
  //Имя комопнента
  name: 'App',
  //Логика выполняемая перед созданием компонента при его вызове
  beforeCreate() {
    //Инициализируем хранилища приложения
    this.$store.commit('initializeStore')
    //Получаем токен авторизации их хранилища браузера
    const token = this.$store.state.token
    if (token) {
      //Если токен существует, то записываем это в данные хранилища, и передаем его в axios
      // по умолчанию при отправке запросов
      axios.defaults.headers.common['Authorization'] = "Token " + token
      // Шлем запрос для получения информации о сотруднике и так же записывае информацию в хранилище
      axios
        .get("/api/v1/workers/")
        .then(response => {
          console.log(response)
          let worker = response.data[0]
          this.$store.commit('setWorker', worker)
          // this.$router.push('/login')
        })
        .catch(error => {
          console.log(error)
        })
    } else {
      axios.defaults.headers.common['Authorization'] = ""
    }
    // console.log(this.$store);
    // console.log(Object.values(this.$store.state.user));
  },
  methods: {
    //Прописываем метод для разавторизации пользователя
    logout() {
      //Передаем на сервер, что мы выходим из учетной записи и токен должен стать неактивным
      axios
        .post("/api/v1/token/logout/")
        .then(response => {
          //Очищаем информацию о токене на стороне пользователя
          axios.defaults.headers.common["Authorization"] = ""
          localStorage.removeItem("username")
          localStorage.removeItem("userid")
          localStorage.removeItem("token")
          this.$store.commit('removeToken')
          this.$router.push('/')
        })
        .catch(error => {
          if (error.response) {
            console.log(JSON.stringify(error.response.data))
          } else if (error.message) {
            console.log(JSON.stringify(error.message))
          } else {
            console.log(JSON.stringify(error))
          }
        })
    }
  }
}
</script>
<!-- Подключаем стили -->
<style lang="scss">
@import "../node_modules/bulma";

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}

#logout {
  color: #2c3e50;
}
</style>
