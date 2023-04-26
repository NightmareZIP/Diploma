<template>
  <CalendarInput />
  <div class="calendar" ref="calendar">
    <CalendarColumn v-for="(value, name, index) in concatenatedData" :key="name" :data="value" :day="days[index]"
      :precision="precision" />
  </div>
</template>

<script>
import CalendarColumn from "../components/CalendarColumn.vue"
import CalendarInput from "../components/CalendarInput.vue"

import * as fn from "../utils"

export default {
  name: "calendar",
  components: { CalendarColumn, CalendarInput },
  props: {
    precision: { type: Number, default: 30 },

    data: Array,
    selected: { type: Date, default: () => new Date() }
  },

  mounted() {
  },

  computed: {
    days() {
      let result = []

      for (var i = 0; i < 7; i++) {
        result.push(fn.addDays(fn.getMonday(new Date()), i))
      }
      return result
    },
    concatenatedData() {
      const roundTime = t => {
        let m = t.getMinutes()
        let h = t.getHours()

        let i = 1
        let ceil = 0
        while (this.precision * i < 60) {
          ceil = this.precision * i
          i++
        }

        if (m > ceil) h++
        m =
          ((((m + this.precision / 2) / this.precision) | 0) * this.precision) %
          60

        t.setHours(h)
        t.setMinutes(m)
        t.setSeconds(0)
        t.setMilliseconds(0)
        return t
      }

      let tmp = {
        mon: [],
        tue: [],
        wed: [],
        thu: [],
        fri: [],
        sat: [],
        sun: []
      }

      if (this.data)
        this.data.forEach(person =>
          person.dates.forEach(date => {
            let start = new Date(date.start.date || date.start.dateTime)
            let end = new Date(date.end.date || date.end.dateTime)
            let weekday = new Date(start)
              .toLocaleString("default", { weekday: "short" })
              .toLowerCase()

            let e = {
              id: date.id,
              color: person.color,

              owner: person,
              e: date,

              grid: {
                start: roundTime(start),
                end:
                  start.getTime() != end.getTime()
                    ? roundTime(end)
                    : roundTime(
                      end.setMinutes(end.getMinutes(), this.precision)
                    ),
                dur:
                  start.getTime() != end.getTime()
                    ? Math.round(fn.diffMinutes(end, start) / this.precision)
                    : Math.round(
                      (fn.diffMinutes(end, start) + this.precision) /
                      this.precision
                    )
              }
            }

            let multievent = []
            if (date.attendees)
              this.data.forEach(p =>
                p.dates.forEach(i => {
                  if (date.attendees)
                    if (i.id === date.id) {
                      multievent.push(p.color)
                    }
                })
              )
            if (multievent.length > 1) {
              let existAlready = tmp[weekday].find(t => t.id == date.id)
              if (!existAlready) {
                e.color = multievent
                tmp[weekday].push(e)
              }
            } else tmp[weekday].push(e)
          })
        )

      return tmp
    }
  }
}
</script>

<style scoped lang="scss">
.calendar {
  display: grid;
  width: 75%;
  margin-left: auto;
  margin-right: 20px;
  color: rgb(161, 153, 153);

  height: 100%;
  // user-select: none;

  grid-template-columns: repeat(7, 1fr);
  grid-template-rows: 300%;
}
</style>
