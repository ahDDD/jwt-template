// 引入 axios
import axios from 'axios'

const STORAGE_KEY = 'cool-e'
const syncedData = {
  user: {},
  token: '',
  expire: {
    refresh: '',
    timeout: ''
  },
  login: false
}

// Sync with local storage.
if (!process.server) {
  if (localStorage.getItem(STORAGE_KEY)) {
    const localData = JSON.parse(localStorage.getItem(STORAGE_KEY))
    Object.keys(localData).forEach(x => {
      syncedData[x] = localData[x]
    })
  }
}

export const state = () => (syncedData)

export const getters = {
  isLogin (state) {
    return state.login
  },
  userName (state) {
    return state.login ? state.user.name : '未登录'
  }
}

export const mutations = {
  UPDATE (state, data) {
    state.user = data.user
    state.token = data.token
    state.expire = data.expire
    state.login = true
    data.login = true
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
  },
  REMOVE (state) {
    state.user = {}
    state.token = ''
    state.login = false
  },
  REFRESH (state, { token, refresh }) {
    state.token = token
    state.expire.refresh = refresh
  }
}

export const actions = {
  login ({ commit }, user) {
    return axios.post('/api/account/login/', user).then(response => {
      const data = response.data
      commit('UPDATE', data)
      return Promise.resolve()
    }).catch(response => {
      return Promise.reject(response.data)
    })
  },
  logout ({ commit }, user) {
    commit('REMOVE')
  },
  refresh ({ commit, state }) {
    return axios.post('api/account/login/',
      { token: state.token })
      .then(response => {
        const data = response.data
        commit('REFRESH', {
          token: data.token,
          refresh: data.refresh
        })
      })
      .catch(response => {
        return Promise.reject(response.data.error)
      })
  }
}
