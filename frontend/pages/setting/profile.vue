<template lang="pug">
.register
  mu-appbar(title="医生资料")
    nuxt-link.nuxt-link-active(to="/" slot="left")
      mu-icon-button(icon="navigate_before" slot="left")
  mu-linear-progress(v-if="loading")
  .register-content
    mu-list
      mu-list-item(title="头像")
        mu-avatar(v-if="user.image", :src="user.img" slot="rightAvatar")
        i(v-else class="material-icons mine-icon" slot="rightAvatar") face
    mu-content-block
      mu-select-field(
        v-model="formData.classify",
        :labelFocusClass="['label-foucs']"
        label="类别",
        :errorText="error.classify"
        fullWidth
        @open="error.classify = ''",
        :maxHeight="300")
        mu-menu-item(v-for="(item, index) in classifyList", :key="index", :value="item[0]", :title="item[0]")
      mu-raised-button(label="保存" @click="save" fullWidth primary)
    vue-core-image-upload(
      :class="['btn', 'btn-primary']",
      :crop="false"
      @imageuploaded="imageuploaded",
      :data="image",
      :max-file-size="5242880",
      compress="50",
      :url="upload.url",
      :headers="upload.headers")
      mu-raised-button(label="上传" fullWidth primary)
  mu-snackbar(
    v-if="snackbar.show",
    :message="snackbar.message"
    action="关闭"
    @actionClick="hideSnackbar"
    @close="hideSnackbar")
</template>

<script>
import { mapGetters } from 'vuex'
import VueCoreImageUpload from 'vue-core-image-upload'

export default {
  async asyncData ({ app }) {
    let data = await app.$axios.$get('/care/get_classify/')
    return { classifyList: data.classify }
  },
  components: {
    'vue-core-image-upload': VueCoreImageUpload
  },
  data () {
    return {
      formData: {
        password: '',
        classify: ''
      },
      error: {
        password: '',
        classify: ''
      },
      validated: false,
      snackbar: {
        show: false,
        message: '',
        time: ''
      },
      loading: false,
      classifyList: [],
      image: {},
      upload: {
        url: '/api/account/profile/15768714216/',
        headers: {
          Authorization: `COOL ${this.$store.state.token}`
        }
      }
    }
  },
  methods: {
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
    },
    imageuploaded (res) {
      if (res.errcode === 0) {
        this.src = res.data.src
      }
    },
    imagechanged (res) {
      console.log(res)
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
