import Vue from 'vue'
import axios from 'axios'

const URL = {
  install (Vue, options) {
    Vue.prototype.url = {
      REGISTER: '/api/account/register/'
    }
  }
}

Vue.use(URL)
Vue.prototype.$http = axios
Vue.prototype._ = require('lodash')