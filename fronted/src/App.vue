<template>
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
export default {
  name: 'App',
  beforeCreate() {
    this.$store.commit('initializeStore')


    const token = this.$store.state.token
    if (token) {
      axios.defaults.headers.common['Authorization'] = "Token " + token
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
    logout() {
      axios
        .post("/api/v1/token/logout/")
        .then(response => {
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
