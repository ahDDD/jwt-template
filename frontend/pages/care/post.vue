<template lang="pug">
.register
  mu-appbar(title="问询")
    nuxt-link.nuxt-link-active(to="/care/classify/" slot="left")
      mu-icon-button(icon="navigate_before")
  mu-linear-progress(v-if="loading")
  mu-list
    mu-sub-header 当前问询医生
    mu-list-item(:title="doctor.name")
      mu-avatar(v-if="doctor.image", :src="`/${doctor.image}`" slot="leftAvatar")
      i(v-else class="material-icons mine-icon" slot="leftAvatar") face
      span(slot="describe")
        span(style="color: rgba(0, 0, 0, .87)") {{ doctor.team }}
        br
        template {{ `${doctor.job} | ${utils.classifyDisplay(doctor.classify)}` }}
  mu-content-block.register-content
    mu-divider
    mu-text-field(
      labelFloat
      label="描述"
      hintText="请输简短描述病征"
      v-model="formData.title",
      :errorText="error.title"
      fullWidth
      @focus="error.title = ''",
      @textOverflow="handleInputOverflow",
      :maxLength="40")
    mu-text-field(
      labelFloat
      label="补充"
      hintText="请补充患者的不舒服的部位、主要症状、持续时间",
      hintTextClass="post-hint-text"
      v-model="formData.detail",
      :errorText="error.detail"
      fullWidth
      @focus="error.detail = ''"
      multiLine,
      :rows="4",
      :rowsMax="6")
    mu-raised-button(label="问询" @click="post" fullWidth primary)
  mu-snackbar(
    v-if="snackbar.show",
    :message="snackbar.message"
    action="关闭"
    @actionClick="hideSnackbar"
    @close="hideSnackbar")
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  data () {
    return {
      formData: {
        title: '',
        detail: ''
      },
      error: {
        title: '',
        detail: ''
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
    validate () {
      if (this.formData.title) {
        this.error.title = this.formData.title.length > 40 ? '超长了' : ''
      } else {
        this.error.title = '不能为空'
      }
      this.error.detail = (this.formData.title.length + this.formData.detail.length) < 15 ? '问询内容过短' : ''
    },
    isValidate () {
      return Object.values(this.error).every(x => x === '')
    },
    async post () {
      this.validate()
      if (this.isValidate()) {
        this.loading = true
        try {
          this.formData.user = this.user.id
          this.formData.doctor = this.doctor.id
          await this.$axios.$post(this.url.POST, this.formData)
          this.loading = false
          this.showSnackbar('问询成功')
          setTimeout(() => { this.$router.push({ name: 'index' }) }, 1500)
        } catch (error) {
          const data = error.response.data
          const message = [].concat.apply([], Object.values(data)).join(',')
          this.loading = false
          this.showSnackbar(`问询失败: ${message}`)
        }
      } else {
        this.showSnackbar('输入有误, 请重新输入')
      }
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
    handleInputOverflow (isOverflow) {
      this.error.title = isOverflow ? '超长了' : ''
    }
  },
  computed: {
    ...mapGetters([
      'doctor',
      'user'
    ])
  }
}
</script>

<style lang="stylus">
.register-content.type
  height 50vh
  display: flex
  flex-direction: column
  padding-top 1.5em
.type-button
  margin-bottom 1em
.post-hint-text
  // word-wrap break-word
  word-break break-all
  width 380px
  overflow auto
</style>
