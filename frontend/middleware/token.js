// 设置刷新有限期
const buffer = 3600 * 1000 * 24 * 2

// const sleep = async function (timeout) {
//   return new Promise((resolve, reject) => {
//     setTimeout(() => {
//       console.log('sleep')
//       return resolve()
//     }, timeout)
//   })
// }

export default async function ({ app, store, error, redirect }) {
  if (store.getters.isLogin) {
    const now = Date.parse(new Date())
    if (now > store.state.expire.timeout) {
      store.commit('REMOVE')
    } else {
      const refreshStart = new Date(store.state.expire.refresh)
      refreshStart.setTime(refreshStart.getTime() - buffer)
      const refreshStartT = Date.parse(refreshStart)
      if (now > store.state.expire.refresh) {
        store.commit('REMOVE')
      } else if (now > refreshStartT) {
        try {
          const data = await app.$axios.$post('/account/refresh/', { token: store.state.token })
          store.commit('REFRESH', data)
        } catch (errors) {
          error({
            message: errors.response.data,
            statusCode: errors.response.status
          })
          store.commit('REMOVE')
        }
      }
    }
  }
}
