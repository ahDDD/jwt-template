<template lang="pug">
.register
  mu-appbar(title="修改个人资料")
    nuxt-link.nuxt-link-active(to="/" slot="left")
      mu-icon-button(icon="navigate_before")
  mu-menu.setting-menu(:autoWidth="false", width="auto")
    mu-menu-item.setting-item(title="姓名" :afterText="userInfo.name" @click="openDialog('姓名')")
    mu-menu-item.setting-item(title="性别" :afterText="userInfo.sex" @click="openDialog('性别')")
    mu-menu-item.setting-item(title="邮箱" :afterText="userInfo.email" @click="openDialog('邮箱')")
    mu-menu-item.setting-item(
      v-if="isNotNormal"
      :title="teamTitle" :afterText="userInfo.team" @click="openDialog(teamTitle)")
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
  mu-dialog(:open="dialog.show" :title="dialog.title" @close="dialog.show = false")
    mu-text-field(v-model="dialog.value" fullWidth required)
    mu-flat-button(slot="actions" @click="dialog.show = false" primary label="取消")
    mu-flat-button(slot="actions" primary @click="close" label="确定")
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  created () {
    this.userInfo = this._.cloneDeep(this.user)
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
      userInfo: {}
    }
  },
  methods: {
    openDialog (key) {
      this.dialog.title = key
      this.dialog.transKey = {
        '姓名': 'name',
        '性别': 'sex',
        '邮箱': 'email',
        '战队': 'team',
        '医院': 'team',
        '职位': 'job',
        '职称': 'job',
        '游戏': 'game'
      }[key]
      this.dialog.value = this._.cloneDeep(this.userInfo[this.dialog.transKey])
      this.$nextTick(() => {
        this.dialog.show = true
      })
    },
    close () {
      this.userInfo[this.dialog.transKey] = this.dialog.value
      this.dialog.show = false
    },
    handleSave () {}
  },
  computed: {
    ...mapGetters('auth', [
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
