import Vue from 'vue'

const URL = {
  install (Vue, options) {
    Vue.prototype.url = {
      REGISTER: '/account/register/',
      LOGIN: '/account/login/',
      USER: '/account/user/',
      PROFILE: '/account/profile/',
      CLASSIFY: '/care/get_classify/'
    }
  }
}

// 设置全局的URL
Vue.use(URL)
// 设置全局this._
Vue.prototype._ = require('lodash')
