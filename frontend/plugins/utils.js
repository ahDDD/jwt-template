import Vue from 'vue'
import moment from 'moment'

const URL = {
  install (Vue, options) {
    Vue.prototype.url = {
      REGISTER: '/account/register/',
      LOGIN: '/account/login/',
      USER: '/account/user/',
      PROFILE: '/account/profile/',
      CLASSIFY: '/care/get_classify/',
      DOCTOR: '/care/doctor/',
      POST: '/care/post/',
      POST_LIST: '/care/post/list/',
      COMMENT: '/care/comment/'
    }
    Vue.prototype.utils = {
      classifyDisplay (classify) {
        return {
          'FCK': '妇产科',
          'MNWK': '泌尿外科',
          'PFK': '皮肤科',
          'GK': '骨科',
          'NFMK': '内分泌科',
          'XXGNK': '心血管内科',
          'SJK': '神经科',
          'XHNK': '消化内科',
          'SZNK': '肾脏内科',
          'YJK': '药剂科',
          'JJK': '急诊科',
          'YK': '眼科',
          'JSXLK': '精神心理科',
          'ZLK': '肿瘤科',
          'EBYHK': '耳鼻咽喉科',
          'FSK': '风湿科',
          'QK': '全科',
          'KQK': '口腔科',
          'HXK': '呼吸科',
          'PTWK': '普通外科',
          'XXWK': '心胸外科',
          'NWK': '脑外科',
          'GDYXWK': '肝胆胰腺外科',
          'CWGCWK': '肠胃肛肠外科',
          'RXWK': '乳腺外科',
          'XYK': '血液科',
          'YXJYK': '影像检验科',
          'GRCRK': '感染传染科',
          'TTMZK': '疼痛&麻醉科'
        }[classify]
      },
      sexDisplay (sex) {
        return {
          'male': '男',
          'female': '女',
          'secret': '保密'
        }[sex]
      }
    }
  }
}

// 设置全局的URL
Vue.use(URL)
// 设置全局this._
Vue.prototype._ = require('lodash')
moment.locale('zh-cn')
Vue.prototype.$moment = moment
