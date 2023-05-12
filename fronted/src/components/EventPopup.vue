<template>
    <div class="modal is-active">
        <div class="modal-background"></div>
        <div class="modal-card" :class="{ disable: !can_edit }">
            <header class="modal-card-head">
                <p class="modal-card-title">{{ event_info.event_name }}</p>
                <button class="delete" aria-label="close" @click="close"></button>
            </header>
            <section class="modal-card-body ">
                <div class="field is-horizontal">
                    <div class="field-label">
                        <label>Название</label>
                    </div>
                    <div class="field-body">
                        <div class="control">
                            <input type="text" name="event_name" class="input" v-model="event_info.event_name">
                        </div>
                    </div>
                </div>
                <div class="field is-horizontal">
                    <div class="field-label">
                        <label has-text-left>Создан</label>
                    </div>
                    <div class="field-body">

                        <div class="control">
                            <p>
                                {{ [event_info.created_by.name, event_info.created_by.last_name,
                                event_info.created_by.surname].join(' ') }}
                            </p>
                        </div>
                    </div>

                </div>
                <div class="field is-horizontal">
                    <div class="field-label">
                        <label>Время и дата</label>
                    </div>
                    <div class="field-body">

                        <div class="control">

                            <input type="datetime" ref='start' name="start" class="input" v-model="event_info.date_from">

                        </div>
                        <div class="control">

                            <input type="datetime" ref='end' name="end" class="input" v-model="event_info.date_to">


                        </div>
                    </div>
                </div>
                <div class="field is-horizontal">
                    <div class="field-label">
                        <label>Частота повторения (дней)</label>
                    </div>
                    <div class="field-body">
                        <div class="control">
                            <input type="text" name="period" class="input" v-model="event_info.period">
                        </div>
                    </div>
                </div>
                <div class="field is-horizontal has-text-left">
                    <div class="field-label">
                        <label>Тип события</label>
                    </div>
                    <div class="field-body">
                        <div class="control">
                            <div class="select">
                                <select v-model="event_info.event_type">
                                    <option disabled value="">Выберите один из вариантов</option>
                                    <option v-for="(type, index) in types" v-bind:key="index" v-bind:value="type">
                                        {{ type.name }}</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="field has-text-left">

                    <div class="field-body">
                        <div class="control">
                            <textarea class="textarea" placeholder="Комментарий" v-model="event_info.comment"></textarea>

                        </div>
                    </div>

                </div>
                <!-- <div class="field has-text-left ">
                    <label class="label ">Участники:</label>
                    <div class="control">
                        <div class="content">

                            <ol v-if="event_info.is_new" type="1">
                                <li v-for="(member, index) in workers" v-bind:key="index">{{ member }}</li>
                            </ol>
                            <ol type="1">
                                <li v-for="(member, index) in event_info.members" v-bind:key="index">{{ member }}</li>
                            </ol>
                        </div>
                    </div>
                </div> -->
                <div class="notification is-danger" v-if="error">
                    <p>Убедитесь, что поля заоплнены корректно</p>
                </div>
            </section>
            <footer v-if="can_edit" class="modal-card-foot">
                <button class="button is-success" @click="save">Сохранить</button>
                <button class="button is-danger" @click="delete_event">Удалить событие</button>
                <button class="button" @click="close">Отменить</button>
            </footer>
        </div>
    </div>
</template>

<script>

import bulmaCalendar from '../../node_modules/bulma-calendar/dist/js/bulma-calendar.min.js';
// import Datepicker from 'vue-bulma-datepicker'
import axios from 'axios'

export default {
    name: "eventpopup",
    components: {
        // Datepicker
    },
    props: {
        is_head: false,
        event_info: {},
        // $store.state.event_info: {
        //     // date_from,
        //     // date_to,
        //     // period,
        //     // is_new,
        //     // type,
        //     // color,
        //     // event_name,
        //     // can_edit,
        //     // created_by,
        //     // members,
        // }


    },
    data() {
        return {
            // event_info: this.$store.state.event_info,
            workers: {
            },
            date: new Date(),
            types: {},
            can_edit: this.event_info.can_edit || this.is_head || this.$store.state.user.id == this.event_info.created_by.user_id,
        }
    },
    mounted() {
        axios
            .get('/api/v1/eventtype/')
            .then(response => {
                this.types = response.data;
            })
            .catch(error => {
                console.log(JSON.stringify(error))
            })


        let options = {
            lang: 'ru',
            displayMode: 'default',
            weekStart: 1,
            startDate: new Date(this.event_info.date_from),
            startTime: new Date(this.event_info.date_from),
            todayLabel: "Сегодня",
            nowLabel: "Сейчас",
            validateLabel: "Подтвердить",
            cancelLabel: "Отменить",
            clearLabel: "Очистить",
            editTimeManually: true,
            minDate: new Date(this.event_info.date_from),
            maxDate: new Date(this.event_info.date_to),

        }

        const calendar_start = bulmaCalendar.attach(this.$refs.start, options)[0]

        calendar_start.on('hide', e => (this.event_info.date_from = new Date(e.data.value()) || null))
        options.startDate = new Date(this.event_info.date_to)
        options.startTime = new Date(this.event_info.date_to)

        const calendar_end = bulmaCalendar.attach(this.$refs.end, options)[0]
        calendar_end.on('hide', e => (this.event_info.date_to = new Date(e.data.value()) || null))
    },
    computed: {
    },
    methods: {
        async save() {
            if (this.$store.state.worker.id) {
                this.event_info.user_id = this.$route.params.id
            }
            let url = '/api/v1/event/'
            if (this.event_info.id != 0) {
                url += this.event_info.id + '/'
                await axios
                    .put(url, this.event_info)
                    .then(response => {
                        this.$store.commit('change_event', this.event_info)
                        console.log(response)
                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
            }
            else {
                if (this.$store.state.worker.id) {
                    this.event_info.user_id = this.$route.params.id
                }
                await axios
                    .post(url, this.event_info)
                    .then(response => {
                        // this.$store.commit('change_event', this.event_info)
                        console.log(response)
                        this.close()

                    })
                    .catch(error => {
                        console.log(JSON.stringify(error))
                    })
            }
        },
        async delete_event() {
            if (this.$store.state.worker.id) {
                this.event_info.user_id = this.$route.params.id
            }
            await axios
                .delete("/api/v1/event/" + this.event_info.id + '/', {
                    headers: {
                        'Content-Type': 'application/json; charset=UTF-8',
                    },
                    data: { user_id: this.$route.params.id }
                })
                .then(response => {
                    this.close()
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
        close() {
            this.$emit('close')
        },
    },
}
</script>

<style lang="scss" scoped>
// Import Bulma core
@import "../../node_modules/bulma-calendar/dist/css/bulma-calendar.min.css";

.modal-card.disable input {
    pointer-events: none;
}
</style>
