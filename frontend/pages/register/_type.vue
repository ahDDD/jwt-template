<template lang="pug">
.register
  mu-appbar(title="注册")
    nuxt-link(to="/register/" slot="left")
      mu-icon-button(icon="navigate_before" slot="left")
  mu-content-block
    mu-text-field(
      labelFloat
      label="用户名"
      hintText="请输入用户名"
      v-model="formData.phone",
      :errorText="error.phone"
      fullWidth)
    mu-text-field(
      labelFloat
      label="密码"
      hintText="请输入密码"
      type="password",
      v-model="formData.password",
      :errorText="error.password"
      fullWidth)
    mu-text-field(
      labelFloat
      label="姓名"
      hintText="请输入真实姓名"
      v-model="formData.name",
      :errorText="error.name"
      fullWidth)
    mu-select-field(
      v-model="formData.sex",
      :labelFocusClass="['label-foucs']"
      label="性别",
      :errorText="error.sex"
      fullWidth)
      mu-menu-item(value="male" title="男")
      mu-menu-item(value="female" title="女")
      mu-menu-item(value="secret" title="保密")
    mu-text-field(
      labelFloat,
      :label="teamLabel",
      :hintText="`请输入${teamLabel}`"
      v-model="formData.team",
      :errorText="error.team"
      fullWidth)
    mu-text-field(
      v-if="this.$route.params.type === 'player'"
      labelFloat
      label="游戏"
      hintText="请输入游戏"
      v-model="formData.game",
      :errorText="error.game"
      fullWidth)
    mu-text-field(
      labelFloat,
      :label="jobLabel",
      :hintText="`请输入${jobLabel}`"
      v-model="formData.job",
      :errorText="error.job"
      fullWidth)
    mu-raised-button(label="注册" @click="register" fullWidth primary)
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
      error: {
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
        defaultIndex: 0,
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
        this.error[x] = this.formData[x] === '' ? '不能为空' : ''
        if (x === 'phone') {
          this.error[x] = isMobilePhone(this.formData[x], 'zh-CN') ? '' : '用户名必须为合法手机号'
        }
      })
    },
    register () {
      this.validate()
      if (this.isValidate()) {
        this.Indicator.open()
        this.$http.post(this.url.REGISTER, {
          ...this.formData
        })
          .then(response => {
            this.Indicator.close()
            this.Toast({
              message: '注册成功'
            })
          })
          .catch(response => {
            this.Indicator.close()
            this.Toast({
              message: '注册失败'
            })
          })
      } else {
        this.Toast({
          message: '输入有误'
        })
      }
    },
    isValidate () {
      return Object.values(this.error).every(x => x === '')
    }
  },
  computed: {
    statePhone () {
      const data = this.formData.phone
      return data ? isMobilePhone(data, 'zh-CN') ? '' : '用户名必须为合法手机号' : '不能为空'
    },
    statePass () {
      const data = this.formData.password
      return data ? '' : '不能为空'
    },
    stateName () {
      const data = this.formData.name
      return data ? '' : '不能为空'
    }
  }
}
</script>

<style lang="stylus">
a
  color white
</style>
