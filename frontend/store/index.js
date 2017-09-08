import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

const STORAGE_KEY = 'cool-e'
const store = () => new Vuex.Store({
  state: {
    user: {},
    token: '',
    expire: {
      refresh: '',
      timeout: ''
    },
    login: false,
    error: {
      message: '',
      name: ''
    },
    // 用户提问的医生
    doctor: {}
  },
  getters: {
    isLogin (state) {
      return state.login
    },
    userName (state) {
      return state.login ? state.user.name : '未登录'
    },
    user (state) {
      return state.user
    },
    error (state) {
      return state.error
    },
    doctor (state) {
      return Object.keys(state.doctor).length > 0 ? state.doctor : ''
    }
  },
  mutations: {
    INIT (state, data) {
      state.user = data.user
      state.token = data.token
      state.expire = data.expire
      state.login = true
      data.login = true
    },
    REMOVE (state) {
      state.user = {}
      state.token = ''
      state.expire = {}
      state.login = false
    },
    REFRESH (state, data) {
      state.token = data.token
      state.expire.refresh = data.expire.refresh
    },
    UPDATE (state, data) {
      Object.keys(data).forEach(x => {
        state.user[x] = data[x]
      })
    },
    SET_ERROR (state, error) {
      state.error = error
    },
    RESET_ERROR (state) {
      state.error = {
        message: '',
        name: ''
      }
    },
    UPDATE_PROFILE (state, { image, classify }) {
      if (image) {
        state.user.image = image
      } else if (classify) {
        state.user.classify = classify
      }
    },
    SET_DOCTOR (state, doctor) {
      state.doctor = doctor
    },
    RESET_DOCTOR (state) {
      state.doctor = {}
    }
  },
  actions: {
    login ({ commit }, user) {
      // try {
      //   const response = await this.$axios.$post('/account/login/', user)
      //   const data = response.data
      //   commit('INIT', data)
      //   return Promise.resolve()
      // } catch (error) {
      //   console.log(error)
      //   return Promise.reject(error.response.data)
      // }
      console.log(this)
      return this.$axios.$post('/api/account/login/', user).then(response => {
        const data = response.data
        commit('INIT', data)
        return Promise.resolve()
      }).catch(error => {
        console.log(error)
        return Promise.reject(error.response.data)
      })
    },
    logout ({ commit }, user) {
      commit('REMOVE')
    },
    update ({ commit, state }, info) {
      Object.keys(info).forEach(x => {
        if (info[x] === state.user[x]) {
          delete info[x]
        }
      })
      return this.$axios.patch(`/api/account/user/${state.user.phone}/`, info)
        .then(response => {
          commit('INIT', info)
          return Promise.resolve()
        })
        .catch(error => {
          return Promise.reject(error.response.data)
        })
    },
    // FIXME: 需要测试
    refresh ({ commit, state }) {
      return this.$axios.post('api/account/login/',
        { token: state.token })
        .then(response => {
          const data = response.data
          commit('REFRESH', {
            token: data.token,
            refresh: data.refresh
          })
          return Promise.resolve()
        })
        .catch(error => {
          return Promise.reject(error.response.data)
        })
    }
  },
  plugins: [createPersistedState({
    key: STORAGE_KEY
  })]
})

export default store

// const STORAGE_KEY = 'cool-e'
// const syncedData = {
//   user: {},
//   token: '',
//   expire: {
//     refresh: '',
//     timeout: ''
//   },
//   login: false
// }

// // Sync with local storage.
// if (!process.server) {
//   if (localStorage.getItem(STORAGE_KEY)) {
//     const localData = JSON.parse(localStorage.getItem(STORAGE_KEY))
//     Object.keys(localData).forEach(x => {
//       syncedData[x] = localData[x]
//     })
//   }
// }

// axios.defaults.headers.common['Authorization'] = `COOL ${syncedData.token}`

// export const state = () => (syncedData)

// export const getters = {
//   isLogin (state) {
//     return state.login
//   },
//   userName (state) {
//     return state.login ? state.user.name : '未登录'
//   },
//   user (state) {
//     return state.user
//   }
// }

// export const mutations = {
//   INIT (state, data) {
//     state.user = data.user
//     state.token = data.token
//     state.expire = data.expire
//     state.login = true
//     data.login = true
//     localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
//   },
//   REMOVE (state) {
//     state.user = {}
//     state.token = ''
//     state.expire = {}
//     state.login = false
//     localStorage.removeItem(STORAGE_KEY)
//   },
//   REFRESH (state, { token, refresh }) {
//     state.token = token
//     state.expire.refresh = refresh
//   },
//   UPDATE (state, data) {
//     Object.keys(data).forEach(x => {
//       state.user[x] = data[x]
//     })
//     localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
//   }
// }

// export const actions = {
//   login ({ commit }, user) {
//     return axios.post('/api/account/login/', user).then(response => {
//       const data = response.data
//       commit('INIT', data)
//       return Promise.resolve()
//     }).catch(error => {
//       return Promise.reject(error.response.data)
//     })
//   },
//   logout ({ commit }, user) {
//     commit('REMOVE')
//   },
//   update ({ commit, state }, info) {
//     Object.keys(info).forEach(x => {
//       if (info[x] === state.user[x]) {
//         delete info[x]
//       }
//     })
//     return axios.patch(`/api/account/user/${state.user.phone}/`, info)
//       .then(response => {
//         commit('INIT', info)
//         return Promise.resolve()
//       })
//       .catch(error => {
//         return Promise.reject(error.response.data)
//       })
//   },
//   // FIXME: 需要测试
//   refresh ({ commit, state }) {
//     return axios.post('api/account/login/',
//       { token: state.token })
//       .then(response => {
//         const data = response.data
//         commit('REFRESH', {
//           token: data.token,
//           refresh: data.refresh
//         })
//         return Promise.resolve()
//       })
//       .catch(error => {
//         return Promise.reject(error.response.data)
//       })
//   }
// }
