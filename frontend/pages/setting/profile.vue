<template lang="pug">
.register
  mu-appbar(title="医生资料")
    nuxt-link.nuxt-link-active(to="/" slot="left")
      mu-icon-button(icon="navigate_before" slot="left")
  mu-linear-progress(v-if="loading")
  .register-content
    mu-list
      mu-list-item(title="头像" @click="openDialog")
        mu-avatar(v-if="user.image", :src="imageSrc" slot="rightAvatar")
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
  mu-dialog(:open="dialog.show", title="上传头像")
    template 请上传尺寸在400*400以下, 大小为50kB以下的图片
    mu-content-block.profile-center(v-if="dialog.loading")
      mu-circular-progress(:size="40")
    vue-core-image-upload(
      v-show="!dialog.loading",
      :crop="false"
      @imageuploaded="imageuploaded",
      @imagechanged="imagechanged",
      @imageuploading="imageuploading",
      @errorhandle="errorhandle",
      :data="image",
      :max-file-size="52428",
      compress="50",
      :url="upload.url",
      :headers="upload.headers",
      :max-width="400",
      :max-height="400")
      mu-raised-button(label="选择" fullWidth primary)
    mu-flat-button(v-if="!dialog.loading" slot="actions" @click="dialog.show = false" primary label="取消")
  mu-snackbar(
    v-if="snackbar.show",
    :message="snackbar.message"
    action="关闭"
    @actionClick="hideSnackbar"
    @close="hideSnackbar")
</template>

<script>
import { mapMutations, mapGetters } from 'vuex'
import VueCoreImageUpload from 'vue-core-image-upload'

export default {
  async asyncData ({ app }) {
    let data = await app.$axios.$get('/care/get_classify/')
    return { classifyList: data.classify }
  },
  components: {
    'vue-core-image-upload': VueCoreImageUpload
  },
  mounted () {
    this.$nextTick(() => {
      this.formData.classify = this.user.classify
    })
  },
  data () {
    return {
      formData: {
        classify: ''
      },
      error: {
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
      dialog: {
        show: false,
        loading: false
      }
    }
  },
  methods: {
    ...mapMutations([
      'UPDATE_PROFILE'
    ]),
    handleClose () {},
    validate () {
      Object.keys(this.formData).forEach(x => {
        this.error[x] = this.formData[x] === '' ? '不能为空' : ''
      })
    },
    async save () {
      this.validate()
      if (this.formData.classify !== this.user.classify) {
        if (this.isValidate()) {
          this.loading = true
          try {
            const data = await this.$axios.$put(`${this.url.PROFILE}${this.user.phone}/`, this.formData)
            this.loading = false
            this.showSnackbar('修改成功')
            this.UPDATE_PROFILE({ classify: data.classify })
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
      } else {
        this.showSnackbar('修改成功')
        setTimeout(() => { this.$router.push({ name: 'index' }) }, 500)
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
      if (res.errcode) {
        this.showSnackbar('上传失败')
        this.dialog.loading = false
      } else {
        this.UPDATE_PROFILE({ image: res.file })
        this.showSnackbar('上传成功')
        this.dialog.loading = false
        this.close()
      }
    },
    imagechanged (res) {
    },
    imageuploading (res) {
      this.dialog.loading = true
    },
    errorhandle (err) {
      this.showSnackbar(err)
    },
    openDialog () {
      this.$nextTick(() => {
        this.dialog.show = true
      })
    },
    close () {
      this.dialog.show = false
    }
  },
  computed: {
    ...mapGetters([
      'user'
    ]),
    upload () {
      return {
        url: `/api/account/profile/${this.user.phone}/image/`,
        headers: {
          Authorization: `COOL ${this.$store.state.token}`
        }
      }
    },
    imageSrc () {
      return this.image.base64Code ? this.image.base64Code : `/${this.user.image}`
    }
  }
}
</script>

<style lang="stylus">
.register-content
  height 90vh
  overflow scroll
.profile-center
  display flex
  justify-content center
</style>
