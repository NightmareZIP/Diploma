<template>
    <table class="table">
        <thead>
            <tr>
                <td>
                    <button v-on:click="decrease">{{ '<' }} </button>
                </td>
                <td colspan="5"> {{ monthes[month] }} {{ year }} </td>
                <td>
                    <button v-on:click="increase">{{ '>' }}</button>
                </td>
            </tr>
            <tr>
                <td v-for="d in day" :key="`${d}`"> {{ d }}</td>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(week, ind) in calendar" :key="`${ind}`">
                <td v-for=" (day_el, ind) in week" :key="`${ind}`"> {{ day_el.index }} </td>
            </tr>
        </tbody>
    </table>
</template>

<script>
export default {
    name: "calendarinput",
    data() {
        return {
            month: new Date().getMonth(),
            year: new Date().getFullYear(),
            dFirstMonth: '1',
            day: ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вск"],
            monthes: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            date: new Date(),

        }
    },
    computed: {
        calendar() {
            let days = [];
            let week = 0;
            days[week] = [];
            let dlast = new Date(this.year, this.month + 1, 0).getDate();
            for (let i = 1; i <= dlast; i++) {
                if (new Date(this.year, this.month, i).getDay() != this.dFirstMonth) {
                    let a = { index: i };
                    days[week].push(a);
                    if (i == new Date().getDate() && this.year == new Date().getFullYear() && this.month == new Date().getMonth()) { a.current = '#747ae6' };
                    if (new Date(this.year, this.month, i).getDay() == 6 || new Date(this.year, this.month, i).getDay() == 0) { a.weekend = '#ff0000' };
                }
                else {
                    week++;

                    days[week] = [];
                    let a = { index: i };
                    days[week].push(a);
                    if ((i == new Date().getDate()) && (this.year == new Date().getFullYear()) && (this.month == new Date().getMonth())) { a.current = '#747ae6' };
                    if (new Date(this.year, this.month, i).getDay() == 6 || new Date(this.year, this.month, i).getDay() == 0) { a.weekend = '#ff0000' };
                }
            }

            if (days[0].length > 0) {
                for (let i = days[0].length; i < 7; i++) {
                    days[0].unshift('');

                }
            }
            console.log(days);
            return days;
        },
    },
    methods: {

        decrease: function () {
            this.month--;
            if (this.month < 0) {
                this.month = 12;
                this.month--;
                this.year--;
            }

        },
        increase: function () {

            this.month++;
            if (this.month > 11) {
                this.month = -1;
                this.month++;
                this.year++;
            }
        },
    },


}
</script>
<style>
.table {
    margin-left: 20px;
    margin-right: 20px;
    border-collapse: collapse;
    float: left;
    position: sticky;
    top: 20%;
    left: 20px;
    right: 20px;

    table-layout: fixed;
}

.format-week {
    float: right;
}

.table td {
    text-align: center;
}

.table thead tr:last-child {
    background-color: #42b983;
}
</style>