<template lang="pug">
.register
  mt-header(title="注册")
    nuxt-link(to="/register/" slot="left")
      mt-button(icon="back")
  .register
    mt-field(label="用户名" placeholder="请输入手机号" v-model="formData.phone", :state="stateDisplay('phone')")
    mt-field(label="密码" placeholder="请输入密码" type="password" v-model="formData.password", :state="stateDisplay('password')")
    mt-field(label="姓名" placeholder="请输入姓名" v-model="formData.name", :state="stateDisplay('name')")
    mt-field(
      readonly,
      label="性别"
      placeholder="请输入性别"
      v-model="formData.sex",
      :state="stateDisplay('phone')"
      @click.native="genderPopup = true")
    mt-field(:label="teamLabel", :placeholder="`请输入${teamLabel}`" v-model="formData.team", :state="stateDisplay('team')")
    mt-field(
      v-if="this.$route.params.type === 'player'",
      label="游戏",
      placeholder="请输入游戏"
      v-model="formData.game",
      :state="stateDisplay('game')")
    mt-field(:label="jobLabel", :placeholder="`请输入${jobLabel}`" v-model="formData.job", :state="stateDisplay('job')")
    mt-button(size="large" @click.native="register") 注册
  mt-popup(v-model="genderPopup" position="bottom")
    mt-picker(:slots="genderSlot" @change="onGenderChange")
</template>

<script>
import isMobilePhone from 'validator/lib/isMobilePhone'

export default {
  created () {
    const type = this.$route.params.type
    this.renderField(type)
    this.formData.user_type = type
  },
  data () {
    return {
      formData: {
        user_type: '',
        phone: '',
        password: '',
        name: '',
        sex: '',
        team: '',
        game: '',
        job: '',
        email: ''
      },
      teamLabel: '',
      jobLabel: '',
      validates: {
        phone: '',
        password: '',
        name: '',
        sex: '',
        team: '',
        game: '',
        job: '',
        email: ''
      },
      validated: false,
      genderPopup: false,
      genderSlot: [{
        values: ['男', '女', '保密']
      }]
    }
  },
  methods: {
    handleClose () {},
    renderField (type) {
      this.teamLabel = type === 'doctor' ? '医院' : '战队'
      this.jobLabel = type === 'doctor' ? '职位' : '职业'
    },
    validate () {
      Object.keys(this.formData).forEach(x => {
        console.log(x)
        this.validates[x] = {
          'phone': isMobilePhone(this.formData[x], 'zh-CN'),
          'password': this.formData[x] ? '' : true
        }[x]
      })
      this.validated = true
    },
    register () {
      this.validate()
      console.log(this.isValidate())
    },
    stateDisplay (key) {
      const data = this.validates[key]
      if (!this.validated) {
        return ''
      } else if (data === '') {
        return 'warning'
      } else {
        return this.validates[key] ? 'success' : 'error'
      }
    },
    isValidate () {
      return Object.values(this.validates).every(x => x)
    },
    onGenderChange (picker, values) {
      // console.log(values)
      this.formData.sex = values[0]
    }
  },
  computed: {
  }
}
</script>

<style lang="stylus">

</style>
