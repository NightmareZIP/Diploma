<template>
    <div class="page-signup">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Регистрация</h1>

                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label>Ваш E-mail</label>
                        <div class="control">
                            <input type="email" name="username" class="input" v-model="username">
                        </div>
                    </div>

                    <div class="field">
                        <label>Пароль</label>
                        <div class="control">
                            <input type="password" name="password" class="input" v-model="password">
                        </div>
                    </div>

                    <div class="field">
                        <label>Имя</label>
                        <div class="control">
                            <input type="text" name="name" class="input" v-model="name">
                        </div>
                    </div>
                    <div class="field">

                        <label>Фамилия</label>
                        <div class="control">
                            <input type="text" name="last_name" class="input" v-model="last_name">
                        </div>
                    </div>
                    <div class="field">

                        <label>Отчество</label>
                        <div class="control">
                            <input type="text" name="surname" class="input" v-model="surname">
                        </div>
                    </div>
                    <div class="field">
                        <label>Телефон</label>
                        <div class="control">
                            <input type="tel" name="contact_phone" class="input" v-model="contact_phone">
                        </div>
                    </div>
                    <div class="field">
                        <label>Страна</label>
                        <div class="control">
                            <input type="text" name="country" class="input" v-model="country">
                        </div>
                    </div>
                    <!-- Данные компании -->
                    <div class="field">
                        <label>Название компании</label>
                        <div class="control">
                            <input type="text" name="cmp_name" class="input" v-model="company_data.name">
                        </div>
                    </div>

                    <div class="field">
                        <label>Страна Компании</label>
                        <div class="control">
                            <input type="text" name="cmp_country" class="input" v-model="company_data.country">
                        </div>
                    </div>

                    <div class="field">
                        <label>Адрес</label>
                        <div class="control">
                            <input type="text" name="place" class="input" v-model="company_data.place">
                        </div>
                    </div>

                    <div class="field">
                        <label>Представитель</label>
                        <div class="control">
                            <input type="text" name="contact_person" class="input" v-model="company_data.contact_person">
                        </div>
                    </div>

                    <div class="field">
                        <label>Контактный телефон</label>
                        <div class="control">
                            <input type="text" name="contact_phone" class="input" v-model="company_data.contact_phone">
                        </div>
                    </div>

                    <div class="field">
                        <label>Контактный e-mail</label>
                        <div class="control">
                            <input type="text" name="cmp_email" class="input" v-model="company_data.email">
                        </div>
                    </div>
                    <div class="field">
                        <label>ИНН</label>
                        <div class="control">
                            <input type="text" name="inn" class="input" v-model="company_data.inn">
                        </div>
                    </div>


                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">
                            {{ error }}
                        </p>
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-success">Зарегестрировать</button>
                        </div>
                    </div>
                </form>

                <hr>

                <router-link to="/login">Нажмите чтобы войти в сущетсвующий аккаунт</router-link>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'CompanyRegister',
    data() {
        return {
            username: '',
            password: '',
            name: '',
            last_name: '',
            surname: '',
            contact_phone: '',
            country: '',
            company_data: {
                name: '',
                country: '',
                place: '',
                contact_person: '',
                contact_phone: '',
                email: '',
                inn: '',
            },
            errors: []
        }
    },
    methods: {
        async submitForm(e) {
            axios.defaults.headers.common["Authorization"] = ""
            localStorage.removeItem("token")
            this.errors = []
            const formData = {
                username: this.username,
                password: this.password
            }

            let user_id = 0;
            //Создаем django пользователя (поля логин и пароль)
            await axios
                .post("/api/v1/users/", formData)
                .then(response => {
                    console.log(response)
                    user_id = response.data.id

                    // this.$router.push('/login')
                })
                .catch(error => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                        console.log(JSON.stringify(error.response.data))
                    } else if (error.message) {
                        console.log(JSON.stringify(error.message))
                    } else {
                        console.log(JSON.stringify(error))
                    }
                })
            console.log('ID ' + user_id)
            //авторизируемся, нужно для записи других данных
            await axios
                .post("/api/v1/token/login/", formData)
                .then(response => {
                    const token = response.data.auth_token
                    this.$store.commit('setToken', token)

                    axios.defaults.headers.common["Authorization"] = "Token " + token
                    localStorage.setItem("token", token)
                })
                .catch(error => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                        console.log(JSON.stringify(error.response.data))
                    } else if (error.message) {
                        console.log(JSON.stringify(error.message))
                    } else {
                        console.log(JSON.stringify(error))
                    }
                })
            const userData = {
                user_id: user_id,
                name: this.name,
                last_name: this.last_name,
                surname: this.surname,
                email: this.username,
                contact_phone: this.contact_phone,
                country: this.country,
                company: this.company_data,
            }
            //Создаем самого работника
            await axios
                .post("/api/v1/workercompany/", userData)
                .then(response => {
                    console.log(response)

                })
                .catch(error => {
                    console.log("ERROR")
                    const deliting = {
                        current_password: formData.password
                    }
                    //В случае неудачи удаляем пользователя django 
                    axios
                        .delete("/api/v1/users/me", { data: deliting, headers: { "Authorization": "Token " + localStorage.getItem("token") } })
                        .then(response => {
                            console.log(response)
                            // this.$router.push('/login')
                        })
                        .catch(error => {
                            if (error.response) {
                                for (const property in error.response.data) {
                                    this.errors.push(`${property}: ${error.response.data[property]}`)
                                }
                                console.log(JSON.stringify(error.response.data))
                            } else if (error.message) {
                                console.log(JSON.stringify(error.message))
                            } else {
                                console.log(JSON.stringify(error))
                            }
                        })
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                        console.log(JSON.stringify(error.response.data))
                    } else if (error.message) {
                        console.log(JSON.stringify(error.message))
                    } else {
                        console.log(JSON.stringify(error))
                    }
                    throw "Oops"
                })
            await axios
                .get("/api/v1/users/me")
                .then(response => {
                    this.$store.commit('setUser', { 'username': response.data.username, 'id': response.data.id })
                    localStorage.setItem('username', response.data.username)
                    localStorage.setItem('userid', response.data.id)
                    this.$router.push('/')
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        }
    }
}
</script>