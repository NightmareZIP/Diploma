import { createStore } from 'vuex'

export default createStore({
  state: {
    user: {
      id: '',
      username: '',
    },
    isAuthenticated: false,
    token: '',
    event_info: {
      id: 0,
      date_start: new Date(),
      date_end: new Date(),
      period: 0,
      color: '',

      type: '',
      event_name: "Новое событие",
      is_new: true,
      can_edit: true,
      created_by: 'Вами',
      members: ['Вы'],
    },
  },
  getters: {
  },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem('token')) {
        state.token = localStorage.getItem('token')
        state.isAuthenticated = true
        state.user.username = localStorage.getItem('username')
        state.user.id = localStorage.getItem('userid')
      } else {
        state.user.id = ''
        state.user.username = ''
        state.token = ''
        state.isAuthenticated = false
      }
      state.worker = ''

    },
    setToken(state, token) {
      state.token = token
      state.isAuthenticated = true
    },
    setWorker(state, worker) {
      state.worker = worker

    },
    removeToken(state) {
      state.user.id = ''
      state.user.username = ''
      state.token = ''
      state.isAuthenticated = false
    },
    setUser(state, user) {
      state.user = user
    },
    change_event(state, info) {
      state.event_info = info
    },
  },
  actions: {
  },
  modules: {
  }
})
