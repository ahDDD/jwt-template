export default function ({ route, store, redirect }) {
  if (!store.getters.isLogin) {
    // 未登录时进入需要登录的页面, 转跳至登录页
    // 以下为不需要登录的页面, 除以下页面以外的页面都跳转至登录
    if (['index', 'login', 'register', 'register-type'].indexOf(route.name) === -1) {
      store.commit('SET_ERROR', { message: '请登录后再执行此操作', name: 'login' })
      return redirect('/login/')
    }
  } else {
    // 登录后进入登录, 注册等页面, 跳转至首页
    if (['login', 'register', 'register-type'].indexOf(route.name) > -1) {
      return redirect('/')
    }
  }
}
