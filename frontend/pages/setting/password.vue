<template lang="pug">
.register
  mu-appbar(title="修改密码")
    nuxt-link.nuxt-link-active(to="/" slot="left")
      mu-icon-button(icon="navigate_before" slot="left")
  mu-linear-progress(v-if="loading")
  mu-content-block.register-content
    mu-text-field(
      labelFloat
      label="原密码"
      hintText="请输入原密码"
      type="password",
      v-model="formData.password",
      :errorText="error.password"
      fullWidth
      @focus="error.password = ''")
    mu-text-field(
      labelFloat
      label="新密码"
      hintText="请输入原密码"
      type="password",
      v-model="formData.newPassword",
      :errorText="error.newPassword"
      fullWidth
      @focus="error.newPassword = ''")
    mu-text-field(
      labelFloat
      label="再次输入新密码"
      hintText="请再次输入原密码"
      type="password",
      v-model="formData.newPassword2",
      :errorText="error.newPassword"
      fullWidth
      @focus="error.newPassword = ''")
    mu-raised-button(label="保存" @click="save" fullWidth primary)
  mu-snackbar(
    v-if="snackbar.show",
    :message="snackbar.message"
    action="关闭"
    @actionClick="hideSnackbar"
    @close="hideSnackbar")
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  mounted () {
  },
  data () {
    return {
      formData: {
        password: '',
        newPassword: '',
        newPassword2: ''
      },
      teamLabel: '',
      jobLabel: '',
      error: {
        password: '',
        newPassword: ''
      },
      validated: false,
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
      'logout'
    ]),
    handleClose () {},
    validate () {
      Object.keys(this.formData).forEach(x => {
        this.error[x] = this.formData[x] === '' ? '不能为空' : ''
        if (x === 'newPassword2') {
          this.error.newPassword = this.formData.newPassword === this.formData.newPassword2 ? '' : '两次输入的密码不一样!'
        }
      })
    },
    async save () {
      this.validate()
      if (this.isValidate()) {
        this.loading = true
        try {
          await this.$axios.$post(`${this.url.USER}${this.user.phone}/set_password/`, this.formData)
          this.loading = false
          this.showSnackbar('修改成功, 请重新登录')
          this.logout()
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
