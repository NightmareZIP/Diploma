<template>
    <h1 class="title">Данные компании</h1>
    <div class="box">
        <form @submit.prevent="submitForm">

            <div class="field is-horizontal">
                <div class="field-label">
                    <label>Название компании</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input :disabled="!is_head" type="text" name="cmp_name" class="input"
                                v-model="company_data.name">
                        </div>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label">
                    <label>Страна Компании</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input :disabled="!is_head" type="text" name="cmp_country" class="input"
                                v-model="company_data.country">
                        </div>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label">
                    <label>Адрес</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input :disabled="!is_head" type="text" name="place" class="input" v-model="company_data.place">
                        </div>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label">
                    <label>Представитель</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control is-horizontal">
                            <input :disabled="!is_head" type="text" name="contact_person" class="input"
                                v-model="company_data.contact_person">
                        </div>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label">
                    <label>Контактный телефон</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control is-horizontal">
                            <input :disabled="!is_head" type="text" name="contact_phone" class="input"
                                v-model="company_data.contact_phone">
                        </div>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label">
                    <label>Контактный e-mail</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control is-horizontal">
                            <input :disabled="!is_head" type="text" name="cmp_email" class="input"
                                v-model="company_data.email">
                        </div>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label">
                    <label>ИНН</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input :disabled="!is_head" type="text" name="inn" class="input" v-model="company_data.inn">
                        </div>
                    </div>
                </div>
            </div>
            <div class="notification is-danger" v-if="error">
                <p>Убедитесь, что поля заоплнены корректно</p>
            </div>
            <button v-if="is_head" class="button is-success" @click="save">Сохранить</button>

        </form>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "CompanyInfo",
    props: {

    },
    data() {
        return {
            company_data: {
                "name": "",
                "country": "",
                "place": "",
                "contact_person": "",
                "contact_phone": "",
                "email": "",
                "inn": "",
                "head": {
                    "id": '',
                    "name": "",
                    "last_name": "",
                    "surname": "",
                    "email": "",
                    "contact_phone": "",
                    "country": "",
                    "created_at": "",
                    "user_id": '',
                    "head": '',
                    "company": ''
                }
            }
            ,
            errors: [],
        }
    },
    computed: {
        is_head() {

            return this.$store.state.worker.is_head
        }
    },
    created() {
        this.get_data()
    },
    methods: {
        async get_data() {
            await axios
                .get("/api/v1/company/")
                .then(response => {
                    console.log(response)
                    this.company_data = response.data[0]
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
                .put("/api/v1/company/" + this.company_data.id + '/', this.company_data)
                .then(response => {
                    console.log(response)
                    this.company_data = response.data[0]
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
