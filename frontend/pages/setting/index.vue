<template lang="pug">
.register
  mu-appbar(title="修改个人资料")
    nuxt-link.nuxt-link-active(to="/" slot="left")
      mu-icon-button(icon="navigate_before")
  mu-linear-progress(v-if="loading")
  mu-menu.setting-menu(:autoWidth="false", width="auto")
    mu-menu-item.setting-item(title="姓名", :afterText="userInfo.name" @click="openDialog('姓名')")
    mu-menu-item.setting-item(title="性别", :afterText="sexDisplay" @click="openDialog('性别')")
    mu-menu-item.setting-item(title="邮箱", :afterText="userInfo.email" @click="openDialog('邮箱')")
    mu-menu-item.setting-item(
      v-if="isNotNormal",
      :title="teamTitle",
      :afterText="userInfo.team"
      @click="openDialog(teamTitle)")
    mu-menu-item.setting-item(
      v-if="userInfo.user_type === 'player'",
      title="游戏",
      :afterText="userInfo.game"
      @click="openDialog('游戏')")
    mu-menu-item.setting-item(
      v-if="isNotNormal",
      :title="jobTitle",
      :afterText="userInfo.job"
      @click="openDialog(jobTitle)")
  mu-content-block
    mu-raised-button(label="保存" @click="handleSave" fullWidth primary)
  dialog-field(:user-info="userInfo" ref="dialog")
  mu-snackbar(
    v-if="snackbar.show",
    :message="snackbar.message"
    action="关闭"
    @actionClick="hideSnackbar"
    @close="hideSnackbar")
</template>

<script>
import { mapMutations, mapGetters } from 'vuex'
import DialogField from '~/components/setting/dialog-field.vue'

export default {
  components: {
    DialogField
  },
  mounted () {
    this.$nextTick(() => {
      this.userInfo = this._.cloneDeep(this.user)
    })
  },
  data () {
    return {
      dialog: {
        show: false,
        value: '',
        key: '',
        title: '',
        transKey: ''
      },
      userInfo: {},
      snackbar: {
        show: false,
        message: '',
        time: ''
      },
      loading: false
    }
  },
  methods: {
    ...mapMutations([
      'UPDATE'
    ]),
    openDialog (key) {
      this.$refs.dialog.openDialog(key)
    },
    async handleSave () {
      this.loading = true
      const info = this._.cloneDeep(this.userInfo)
      Object.keys(info).forEach(x => {
        if (info[x] === this.user[x]) {
          delete info[x]
        }
      })
      if (Object.keys(info).length === 0) {
        this.loading = false
        this.showSnackbar('修改成功')
        setTimeout(() => { this.$router.push({ name: 'index' }) }, 1500)
      } else {
        try {
          const data = await this.$axios.$patch(`${this.url.USER}${this.user.phone}/`, info)
          this.UPDATE(data)
          this.loading = false
          this.showSnackbar('修改成功')
          setTimeout(() => { this.$router.push({ name: 'index' }) }, 1500)
        } catch (error) {
          const data = error.response.data
          const message = [].concat.apply([], Object.values(data)).join(',')
          this.loading = false
          this.showSnackbar(`修改失败: ${message}`)
        }
      }
    },
    showSnackbar (message) {
      this.snackbar.message = message
      this.snackbar.show = true
      if (this.snackbar.time) clearTimeout(this.snackbar.time)
      this.snackbar.time = setTimeout(() => { this.snackbar.show = false }, 1500)
    },
    hideSnackbar () {
      this.snackbar.show = false
      if (this.snackbar.time) clearTimeout(this.snackbar.time)
    }
  },
  computed: {
    ...mapGetters([
      'isLogin',
      'user'
    ]),
    teamTitle () {
      return this.user.user_type === 'player' ? '战队' : '医院'
    },
    jobTitle () {
      return this.user.user_type === 'player' ? '职位' : '职称'
    },
    isNotNormal () {
      return ['player', 'doctor'].indexOf(this.user.user_type) > -1
    },
    sexDisplay () {
      return {
        'male': '男',
        'female': '女',
        'secret': '保密'
      }[this.userInfo.sex]
    }
  }
}
</script>

<style lang="stylus">
.setting-menu
  padding-top 1.5em
.setting-item
  margin-bottom 1em
</style>
