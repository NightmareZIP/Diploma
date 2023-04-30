<template>
    <div class="modal is-active">
        <div class="modal-background"></div>
        <div class="modal-card" :class="{ disable: !event_info.can_edit }">
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
                            <p>{{ event_info.created_by }}</p>
                        </div>
                    </div>

                </div>
                <div class="field is-horizontal">
                    <div class="field-label">
                        <label>Время и дата</label>
                    </div>
                    <div class="field-body">

                        <div class="control">
                            <!-- <datepicker v-model="event_info.date_start" placeholder="European Format ('d-m-Y')"
                                :config="{ type: 'datetime', lang: 'ru', dateFormat: 'd-m-Y', static: true }">
                            </datepicker> -->
                            <input type="datetime" ref='start' name="start" class="input" v-model="event_info.date_start">

                        </div>
                        <div class="control">
                            <!-- <datepicker v-model="event_info.date_end" placeholder="European Format ('d-m-Y')"
                                :config="{ type: 'datetime', lang: 'ru', dateFormat: 'd-m-Y', static: true }">
                            </datepicker> -->
                            <input type="datetime" ref='end' name="end" class="input" v-model="event_info.date_end">


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
                <div class="field has-text-left ">
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
                </div>
                <div class="notification is-danger" v-if="error">
                    <p>Убедитесь, что поля заоплнены корректно</p>
                </div>
            </section>
            <footer v-if="event_info.can_edit" class="modal-card-foot">
                <button class="button is-success" @click="save">Сохранить</button>
                <button class="button is-danger" @click="delete_event">Сохранить</button>
                <button class="button" @click="close">Отменить</button>
            </footer>
        </div>
    </div>
</template>

<script>

import bulmaCalendar from '../../node_modules/bulma-calendar/dist/js/bulma-calendar.min.js';
import Datepicker from 'vue-bulma-datepicker'
export default {
    name: "eventpopup",
    components: {
        Datepicker
    },
    props: {

        // $store.state.event_info: {
        //     // date_start,
        //     // date_end,
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
            event_info: this.$store.state.event_info,
            workers: {
            },
            date: new Date(),
        }
    },
    mounted() {
        let options = {
            lang: 'ru',
            displayMode: 'default',
            weekStart: 1,
            startDate: this.event_info.date_start,
            todayLabel: "Сегодня",
            nowLabel: "Сейчас",
            validateLabel: "Подтвердить",
            cancelLabel: "Отменить",
            clearLabel: "Очистить",
            editTimeManually: true,
        }

        const calendar_start = bulmaCalendar.attach(this.$refs.start, options)[0]
        console.log(calendar_start);

        calendar_start.on('hide', e => (this.event_info.date_start = new Date(e.data.value()) || null))
        options.startDate = this.event_info.date_end
        const calendar_end = bulmaCalendar.attach(this.$refs.end, options)[0]
        calendar_end.on('hide', e => (this.event_info.date_end = new Date(e.data.value()) || null))
    },
    computed: {
    },
    methods: {
        async save() {
            await axios
                .post("/api/v1/token/change_event/", this.event_info)
                .then(response => {
                    this.$store.commit('change_event', this.event_info)

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
        async delete_event() {
            await axios
                .post("/api/v1/token/delete_event/", this.event_info.id)
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
