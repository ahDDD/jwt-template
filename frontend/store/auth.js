// 引入 axios
import axios from 'axios'

export const state = () => ({
  user: {},
  token: '',
  expire: {
    refresh: '',
    timeout: ''
  },
  login: false
})

export const mutations = {
  UPDATE (state, { user, token, expire }) {
    state.user = user
    state.token = token
    state.expire = expire
    state.login = true
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
      commit('UPDATE', {
        user: data.user,
        token: data.token,
        expire: data.expire
      })
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
