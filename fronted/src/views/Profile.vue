<template>
    <h1 class="title">Ваши данные</h1>
    <div class="box">
        <form @submit.prevent="submitForm">

            <div class="field is-horizontal">
                <div class="field-label">
                    <label>E-mail</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input disabled readonly="readonly" type="email" name="username" class="input"
                                v-model="user_info.email">
                        </div>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label">
                    <label>Имя</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input type="text" name="name" class="input" v-model="user_info.name">
                        </div>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label">
                    <label>Фамилия</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input type="text" name="last_name" class="input" v-model="user_info.last_name">
                        </div>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label">
                    <label>Отчество</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control is-horizontal">
                            <input type="text" name="surname" class="input" v-model="user_info.surname">
                        </div>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label">
                    <label>Компания</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control is-horizontal">
                            <input disabled readonly="readonly" type="text" name="surname" class="input"
                                v-model="user_info.company.name">
                        </div>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label">
                    <label>Телефон</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input type="tel" name="contact_phone" class="input" v-model="user_info.contact_phone">
                        </div>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label">
                    <label>Страна</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input type="text" name="country" class="input" v-model="user_info.country">
                        </div>
                    </div>
                </div>
            </div>
            <div class="notification is-danger" v-if="error">
                <p>Убедитесь, что поля заоплнены корректно</p>
            </div>
            <button class="button is-success" @click="save">Сохранить</button>

        </form>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "Profile",
    props: {
        data: Object
    },
    data() {
        return {
            user_info: {},
            errors: [],
        }
    },
    computed: {

    },
    created() {
        this.get_data()
    },
    methods: {
        async get_data() {
            await axios
                .get("/api/v1/workers/")
                .then(response => {
                    console.log(response)
                    this.user_info = response.data[0]
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
        },
        async save() {
            this.errors = []
            await axios
                .put("/api/v1/workers/" + this.user_info.id + '/', this.user_info)
                .then(response => {
                    console.log(response)
                    this.user_info = response.data[0]
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

        }
    },
}
</script>
