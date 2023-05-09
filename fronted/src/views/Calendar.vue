<template>
  <CalendarInput @changeDay="reloadColumns" />
  <CalendarWeek @newEvent="newEvent" @showPopup="showEvent" :key="reload" ref="calendar" :selected="selected_day"
    :concatenatedData="weekData" :precision="precision">
  </CalendarWeek>
  <EventPopup @close="show_popup = false" v-if="show_popup" :event_info="event_info" />
</template>

<script>
import CalendarInput from "../components/CalendarInput.vue"
import CalendarWeek from "../components/CalendarWeek.vue"
import EventPopup from "../components/EventPopup.vue"


import * as fn from "../utils"
import axios from 'axios'

export default {
  name: "calendar",
  components: { CalendarWeek, CalendarInput, EventPopup },
  data() {
    return {
      event_info: {
        id: 0,
        date_start: new Date(),
        date_end: new Date(),
        period: 0,
        color: '',
        type: {
          id: 2,
          name: 'Больничный',
          color: 'red',
        },
        event_name: "Новое событие",
        is_new: true,
        can_edit: true,
        created_by: 'Вами',
        members: ['Вы'],
      },
      // reload: { type: Number, default: () => 0 },
      selected_day: new Date(),
      show_popup: false,

      // data: Array(),
      data: [
        {
          // id: "test-user2e@test-email.ai",
          // summary: "description ....",
          // color: "#cd74e6",

          id: "1",
          color: "#cd74e6",
          type: {
            id: 3,
            name: 'Другое',
            color: '#cd74e6',
          }, description: 'DESC',
          event_name: "Новое событие",
          date_start: new Date(2023, 3, 26, 3, 0, 0),
          date_end: new Date(2023, 3, 26, 23, 59, 0),
          can_edit: true,
          created_by: 'Вами',
          members: ['Вы'],
        },
        {
          id: "2",
          event_name: "3adasdasd safsf s ewewr w q",

          color: "blue",
          type: {
            id: 2,
            name: 'Больничный',
            color: 'red',
          },
          description: 'DESC',
          date_start: new Date(2023, 3, 26, 1, 0, 0),
          date_end: new Date(2023, 3, 26, 5, 59, 0),
          can_edit: true,
          created_by: 'Вами',
          members: ['Вы'],
        },
        {


          color: "red",
          event_name: "2",
          type: {
            id: 1,
            name: 'Отгул',
            color: 'blue',
          },
          id: "3",
          date_start: new Date(2023, 3, 26, 3, 0, 0),
          date_end: new Date(2023, 3, 26, 23, 59, 0),
          can_edit: true,
          created_by: 'Вами',
          members: ['Вы'],
        },
      ],
    }
  },

  props: {
    precision: {
      type: Number, default: 1
    },

    // selected_day: { type: Date, default: () => new Date() }
  },

  mounted() {
    axios
      .get("/api/v1/event")
      .then(response => {
        console, log(responce)
      })
      .catch(error => {
        console.log(JSON.stringify(error))
      })
  },
  methods: {
    newEvent(n = 0, time = new Date()) {
      console.log(n)
      time.setHours(n, 0, 0)
      this.event_info = {
        id: 0,
        date_start: time,
        date_end: time,
        period: 0,
        color: '',
        type: '',
        event_name: "Новое событие",
        is_new: true,
        can_edit: true,
        created_by: 'Вами',
        members: ['Вы'],

      }
      this.show_popup = true

    },
    reloadColumns(day) {
      this.selected_day = day.date

      // this.reload += 1
    },

    showEvent(id) {
      let copy_events = [...this.data]
      let event = copy_events.filter(e => e.id == id)[0]
      event.is_new = false
      this.event_info = event

      this.show_popup = true

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
        this.data.forEach(date => {
          let start = new Date(date.date_start.date || date.date_start)
          let end = new Date(date.date_end.date || date.date_end)
          let weekday = new Date(start)
            .toLocaleString("default", { weekday: "short" })
            .toLowerCase()

          let e = {
            id: date.id,
            color: date.type.color,

            owner: date.created_by,
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

      return tmp
    }
  }
}
</script>


