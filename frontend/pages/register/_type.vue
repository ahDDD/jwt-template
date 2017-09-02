<template lang="pug">
.register
  mu-appbar(title="注册")
    nuxt-link(to="/register/" slot="left")
      mu-icon-button(icon="navigate_before" slot="left")
  mu-linear-progress(v-if="loading")
  mu-content-block.register-content
    mu-text-field(
      labelFloat
      label="用户名"
      hintText="请输入用户名"
      v-model="formData.phone",
      :errorText="error.phone"
      fullWidth
      @focus="error.phone = ''")
    mu-text-field(
      labelFloat
      label="密码"
      hintText="请输入密码"
      type="password",
      v-model="formData.password",
      :errorText="error.password"
      fullWidth
      @focus="error.password = ''")
    mu-text-field(
      labelFloat
      label="姓名"
      hintText="请输入真实姓名"
      v-model="formData.name",
      :errorText="error.name"
      fullWidth
      @focus="error.name = ''"
      @textOverflow="handleNameOverflow"
      :maxLength="10")
    mu-select-field(
      v-model="formData.sex",
      :labelFocusClass="['label-foucs']"
      label="性别",
      :errorText="error.sex"
      fullWidth
      @open="error.sex = ''")
      mu-menu-item(value="male" title="男")
      mu-menu-item(value="female" title="女")
      mu-menu-item(value="secret" title="保密")
    mu-text-field(
      v-if="this.$route.params.type !== 'normal'"
      labelFloat,
      :label="teamLabel",
      :hintText="`请输入${teamLabel}`"
      v-model="formData.team",
      :errorText="error.team"
      fullWidth
      @focus="error.team = ''")
    mu-text-field(
      v-if="this.$route.params.type === 'player'"
      labelFloat
      label="游戏"
      hintText="请输入游戏"
      v-model="formData.game",
      :errorText="error.game"
      fullWidth
      @focus="error.game = ''")
    mu-text-field(
      v-if="this.$route.params.type !== 'normal'"
      labelFloat,
      :label="jobLabel",
      :hintText="`请输入${jobLabel}`"
      v-model="formData.job",
      :errorText="error.job"
      fullWidth
      @focus="error.job = ''")
    mu-text-field(
      labelFloat,
      label="邮箱",
      hintText="请输入邮箱"
      v-model="formData.email",
      :errorText="error.email"
      fullWidth
      @focus="error.email = ''")
    mu-raised-button(label="注册" @click="register" fullWidth primary)
  mu-snackbar(
    v-if="snackbar.show",
    :message="snackbar.message"
    action="关闭"
    @actionClick="hideSnackbar"
    @close="hideSnackbar")
</template>

<script>
import isMobilePhone from 'validator/lib/isMobilePhone'
import isEmail from 'validator/lib/isEmail'

export default {
  validate ({ params }) {
    console.log(params)
    return ['doctor', 'normal', 'player'].indexOf(params.type) > -1
  },
  created () {
    const type = this.$route.params.type
    this.renderField(type)
    this.formData.user_type = type
    if (type === 'player') {
      ['game', 'job', 'team'].forEach(x => {
        this.formData[x] = ''
        this.error[x] = ''
      })
    } else if (type === 'doctor') {
      ['job', 'team'].forEach(x => {
        this.formData[x] = ''
        this.error[x] = ''
      })
    }
  },
  data () {
    return {
      formData: {
        user_type: '',
        phone: '',
        password: '',
        name: '',
        sex: '',
        email: ''
      },
      teamLabel: '',
      jobLabel: '',
      error: {
        phone: '',
        password: '',
        name: '',
        sex: '',
        email: ''
      },
      validated: false,
      genderPopup: false,
      genderSlot: [{
        defaultIndex: 0,
        values: ['男', '女', '保密']
      }],
      snackbar: {
        show: false,
        message: '',
        time: ''
      },
      loading: false
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
        } else if (x === 'email') {
          this.error[x] = isEmail(this.formData[x]) ? '' : '请输入合法邮箱'
        }
      })
    },
    register () {
      this.validate()
      if (this.isValidate()) {
        this.loading = true
        this.$http.post(this.url.REGISTER, {
          ...this.formData
        })
          .then(response => {
            this.loading = false
            this.showSnackbar('注册成功')
          })
          .catch(response => {
            this.loading = false
            this.showSnackbar('注册失败')
          })
      } else {
        this.showSnackbar('输入有误, 请重新输入')
      }
    },
    isValidate () {
      return Object.values(this.error).every(x => x === '')
    },
    handleNameOverflow (isOverflow) {
      this.error.name = isOverflow ? '过长了' : ''
    },
    showSnackbar (message) {
      this.snackbar.message = message
      this.snackbar.show = true
      if (this.snackbar.time) clearTimeout(this.snackbar.time)
      this.snackbar.time = setTimeout(() => { this.snackbar.show = false }, 2000)
    },
    hideSnackbar () {
      this.snackbar.show = false
      if (this.snackbar.time) clearTimeout(this.snackbar.time)
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
.register-content
  height 90vh
  overflow scroll
</style>
