<template lang="pug">
.register
  mu-appbar(title="登录")
    nuxt-link(to="/" slot="left")
      mu-icon-button(icon="navigate_before")
    nuxt-link(to="/register/" slot="right")
      mu-flat-button(color="white" label="注册")
  mu-linear-progress(v-if="loading")
  mu-content-block.login-content.type
    mu-text-field(
      labelFloat
      label="用户名"
      hintText="请输入手机号"
      v-model="formData.phone",
      :errorText="error.phone"
      fullWidth
      @focus="error.phone = ''")
    mu-text-field(
      labelFloat
      label="密码"
      hintText="请输入8-16位密码"
      type="password",
      v-model="formData.password",
      :errorText="error.password"
      fullWidth
      @focus="error.password = ''")
    mu-raised-button.login-button(label="登录" @click="handleLogin" fullWidth primary)
  mu-snackbar(
    v-if="snackbar.show",
    :message="snackbar.message"
    action="关闭"
    @actionClick="hideSnackbar"
    @close="hideSnackbar")
  nuxt-link.find-button(to="/" slot="left")
    mu-flat-button(label="忘记密码?")
</template>

<script>
import { mapActions } from 'vuex'
import isMobilePhone from 'validator/lib/isMobilePhone'

export default {
  data () {
    return {
      formData: {
        phone: '',
        password: ''
      },
      error: {
        phone: '',
        password: ''
      },
      snackbar: {
        show: false,
        message: '',
        time: ''
      },
      loading: false
    }
  },
  methods: {
    ...mapActions([
      'login'
    ]),
    validate () {
      Object.keys(this.formData).forEach(x => {
        this.error[x] = this.formData[x] === '' ? '不能为空' : ''
        if (x === 'phone') {
          this.error[x] = isMobilePhone(this.formData[x], 'zh-CN') ? '' : '用户名必须为合法手机号'
        }
      })
    },
    isValidate () {
      return Object.values(this.error).every(x => x === '')
    },
    handleLogin () {
      this.validate()
      if (this.isValidate()) {
        this.loading = true
        this.login(this.formData).then(() => {
          this.loading = false
          this.showSnackbar('登录成功, 跳转至首页')
          setTimeout(() => { this.$router.push({ name: 'index' }) }, 1500)
        }).catch(data => {
          this.loading = false
          this.showSnackbar(`登录失败: ${data.non_field_errors.join(',')}`)
        })
      } else {
        this.showSnackbar('输入有误, 请重新输入')
      }
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
  }
}
</script>

<style lang="stylus">
.login-content.type
  padding-top 1.5em
.type-button
  margin-bottom 1em
.login-button
  margin-top 2.5em
.find-button
  // display: flex
  // justify-content: flex-end
  float right
</style>
