<template lang="pug">
.register
  mu-appbar(title="忘记密码")
    nuxt-link(to="/" slot="left")
      mu-icon-button(icon="navigate_before")
  mu-linear-progress(v-if="loading")
  mu-content-block.login-content.type
    mu-text-field(
      labelFloat
      label="用户名"
      hintText="请输入手机号"
      v-model="formData.user",
      :errorText="error.user"
      fullWidth
      @focus="error.user = ''")
    mu-raised-button.login-button(label="发送邮件" @click="handleLogin" fullWidth primary)
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
  data () {
    return {
      formData: {
        user: ''
      },
      error: {
        user: ''
      },
      snackbar: {
        show: false,
        message: '',
        time: ''
      },
      loading: false
    }
  },
  mounted () {
  },
  methods: {
    validate () {
      Object.keys(this.formData).forEach(x => {
        this.error[x] = this.formData[x] === '' ? '不能为空' : ''
        if (x === 'user') {
          this.error[x] = isMobilePhone(this.formData[x], 'zh-CN') ? '' : '用户名必须为合法手机号'
        }
      })
    },
    isValidate () {
      return Object.values(this.error).every(x => x === '')
    },
    async handleLogin () {
      this.validate()
      if (this.isValidate()) {
        this.loading = true
        try {
          await this.$axios.$post(this.url.FORGOT, this.formData)
          this.loading = false
          this.showSnackbar('邮件已发送, 请查收邮件')
          setTimeout(() => { this.$router.push({ name: 'index' }) }, 1500)
        } catch (error) {
          const data = error.response.data
          this.loading = false
          this.showSnackbar(`发送失败: ${data.non_field_errors.join(',')}`)
        }
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
    ...mapGetters({
      globalError: 'error'
    })
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
