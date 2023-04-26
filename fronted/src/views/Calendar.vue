<template>
  <CalendarInput @changeDay="reloadColumns" />
  <CalendarWeek :key="reload" ref="calendar" :selected="selected_day" :concatenatedData="weekData" :precision="precision">
  </CalendarWeek>
  />
</template>

<script>
import CalendarInput from "../components/CalendarInput.vue"
import CalendarWeek from "../components/CalendarWeek.vue"

import * as fn from "../utils"

export default {
  name: "calendar",
  components: { CalendarWeek, CalendarInput },
  data() {
    return {
      // reload: { type: Number, default: () => 0 },
      selected_day: new Date(),
      // data: Array(),
      data: [
        {
          id: "test-user2e@test-email.ai",
          summary: "description ....",
          color: "#cd74e6",
          dates: [
            {
              id: "7413lef3g1hip8hvk6tbipkqrq_20200917T140000Z",
              summary: "event name",
              start: { dateTime: new Date(2023, 3, 26, 3, 0, 0) },
              end: { dateTime: new Date(2023, 3, 26, 23, 59, 0) }
            },
            {
              id: "7413lef3g1hip8hvk6tbipkqrq_20200917T140000Z",
              summary: "event2",
              start: { dateTime: new Date(2023, 3, 26, 1, 0, 0) },
              end: { dateTime: new Date(2023, 3, 26, 5, 59, 0) }
            }
          ]
        },
        {
          id: "test-user2e@test-email.ai",
          summary: "description ....",
          color: "red",
          dates: [
            {
              id: "7413lef3g1hip8hvk6tbipkqrq_20200917T140000Z",
              summary: "event name",
              start: { dateTime: new Date(2023, 3, 26, 3, 0, 0) },
              end: { dateTime: new Date(2023, 3, 26, 23, 59, 0) }
            },

          ]
        }
      ]
    }
  },
  props: {
    precision: { type: Number, default: 1 },
    // selected_day: { type: Date, default: () => new Date() }
  },

  mounted() {
  },
  methods: {
    reloadColumns(day) {
      this.selected_day = day.date

      // this.reload += 1
    }
  },
  computed: {

    weekData() {
      const roundTime = t => {
        let m = t.getMinutes()
        let h = t.getHours()

        let i = 1
        // let ceil = 0
        // while (this.precision * i < 60) {
        //   ceil = this.precision * i
        //   i++
        // }

        // if (m > ceil) h++
        // m =
        //   ((((m + this.precision / 2) / this.precision) | 0) * this.precision) %
        //   60

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
              console.log('MMMM')
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


