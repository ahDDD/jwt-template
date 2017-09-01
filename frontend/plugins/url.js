import Vue from 'vue'
import axios from 'axios'

const URL = {
  install (Vue, options) {
    Vue.prototype.url = {
      REGISTER: '/api/register/'
    }
  }
}

Vue.use(URL)
Vue.prototype.$http = axios
