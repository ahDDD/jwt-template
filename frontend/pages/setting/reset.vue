<template lang="pug">
.register
  mu-appbar(title="重置密码")
    nuxt-link.nuxt-link-active(to="/" slot="left")
      mu-icon-button(icon="navigate_before" slot="left")
  mu-linear-progress(v-if="loading")
  mu-content-block.register-content
    mu-text-field(
      labelFloat
      label="用户名"
      hintText="请输入注册时输入的手机号"
      v-model="formData.user",
      :errorText="error.user"
      fullWidth
      @focus="error.user = ''")
    mu-text-field(
      labelFloat
      label="新密码"
      hintText="请输入原密码"
      type="password",
      v-model="formData.password",
      :errorText="error.password"
      fullWidth
      @focus="error.password = ''")
    mu-text-field(
      labelFloat
      label="再次输入新密码"
      hintText="请再次输入原密码"
      type="password",
      v-model="formData.newPassword2",
      :errorText="error.newPassword2"
      fullWidth
      @focus="error.newPassword2 = ''")
    mu-raised-button(label="保存" @click="save" fullWidth primary)
  mu-snackbar(
    v-if="snackbar.show",
    :message="snackbar.message"
    action="关闭"
    @actionClick="hideSnackbar"
    @close="hideSnackbar")
</template>

<script>
import { mapGetters } from 'vuex'
import isMobilePhone from 'validator/lib/isMobilePhone'

export default {
  async asyncData ({ query, error }) {
    if (query.token.length !== 137) {
      error({ message: 'token有误' })
    } else {
      return { token: query.token }
    }
  },
  mounted () {
  },
  data () {
    return {
      formData: {
        user: '',
        password: '',
        newPassword2: ''
      },
      teamLabel: '',
      jobLabel: '',
      error: {
        password: '',
        newPassword2: '',
        user: ''
      },
      validated: false,
      snackbar: {
        show: false,
        message: '',
        time: ''
      },
      loading: false,
      token: ''
    }
  },
  methods: {
    handleClose () {},
    validate () {
      Object.keys(this.formData).forEach(x => {
        if (x === 'newPassword2') {
          if (this.formData.password && this.formData.password !== this.formData.newPassword2) {
            this.error.password = '两次输入的密码不一样!'
            this.error.newPassword2 = '两次输入的密码不一样!'
          }
        } else if (x === 'phone') {
          this.error[x] = isMobilePhone(this.formData[x], 'zh-CN') ? '' : '用户名必须为合法手机号'
        }
        this.error[x] = this.formData[x] === '' ? '不能为空' : ''
      })
    },
    async save () {
      this.validate()
      if (this.isValidate()) {
        this.loading = true
        try {
          let token = this.replaceChat(this.token, 36, '.')
          token = this.replaceChat(token, 93, '.')
          this.formData.token = token
          await this.$axios.$post(this.url.RESET, this.formData)
          this.loading = false
          this.showSnackbar('修改成功, 请重新登录')
          setTimeout(() => { this.$router.push({ name: 'index' }) }, 1500)
        } catch (error) {
          const data = error.response.data
          const message = [].concat.apply([], Object.values(data)).join(',')
          this.loading = false
          this.showSnackbar(`修改失败: ${message}`)
        }
      } else {
        this.showSnackbar('输入有误, 请重新输入')
      }
    },
    isValidate () {
      return Object.values(this.error).every(x => x === '')
    },
    showSnackbar (message) {
      this.snackbar.message = message
      this.snackbar.show = true
      if (this.snackbar.time) clearTimeout(this.snackbar.time)
      this.snackbar.time = setTimeout(() => { this.snackbar.show = false }, 2500)
    },
    hideSnackbar () {
      this.snackbar.show = false
      if (this.snackbar.time) clearTimeout(this.snackbar.time)
    },
    replaceChat (source, pos, newChar) {
      const sFrontPart = source.substr(0, pos)
      const sTailPart = source.substr(pos + 1, source.length)
      return sFrontPart + newChar + sTailPart
    }
  },
  computed: {
    ...mapGetters([
      'user'
    ])
  }
}
</script>

<style lang="stylus">
.register-content
  height 90vh
  overflow scroll
</style>
