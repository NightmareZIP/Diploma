import { createStore } from 'vuex'

export default createStore({
  //Создаем хранилище с именем state
  state: {
    //Vbybvfkmyfz byajhvfwbz j gjkmpjdfntkt
    user: {
      id: '',
      username: '',
    },
    //Признак авторизации
    isAuthenticated: false,
    //Токе
    token: '',
    //Информация по текущему просматриваему событию для комопнента календаря
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
    },
  },
  getters: {
  },
  mutations: {
    //Любое измененеие хранила реализуется через специальные методы мутаций
    //Инициализация хранилища, проверяем, есть ли в localStorage информация о токене
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
    //Установка токена
    setToken(state, token) {
      state.token = token
      state.isAuthenticated = true
    },
    // Установка данных работник
    setWorker(state, worker) {
      state.worker = worker

    },
    //Удаление токена
    removeToken(state) {
      state.user.id = ''
      state.user.username = ''
      state.token = ''
      state.isAuthenticated = false
    },
    //Установка минимальной информации пользователя
    setUser(state, user) {
      state.user = user
    },
    //Смена текущего просмтариваемого события
    change_event(state, info) {
      state.event_info = info
    },
  },
  actions: {
  },
  modules: {
  }
})
