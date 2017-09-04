import Vue from 'vue'
// import axios from 'axios'

const URL = {
  install (Vue, options) {
    Vue.prototype.url = {
      REGISTER: '/api/account/register/'
    }
  }
}

// 设置全局的URL
Vue.use(URL)
// 设置全局this._
Vue.prototype._ = require('lodash')
// 设置axios的Token
// 设置全局this.$http
// Vue.prototype.$http = axios
