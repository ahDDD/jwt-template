<template lang="pug">
div
  .top
    nuxt-link.mine-avatar-center(:to="avatarPath")
      mu-paper(class="mine-paper" circle :zDepth="4")
        i(class="material-icons mine-icon") face
      mu-flat-button.mine-avatar-button(:label="`你好, ${userName}`" color="white")
  .settings
    mu-content-block
      mu-menu.mine-menu(:autoWidth="false", width="auto")
        template(v-if="isLogin")
          mu-menu-item(title="修改个人资料" rightIcon="keyboard_arrow_right")
          mu-divider
          mu-menu-item(title="关于我们" rightIcon="keyboard_arrow_right")
          mu-divider
          mu-menu-item(title="退出登录" rightIcon="keyboard_arrow_right" @click="logout")
        template(v-else)
          mu-menu-item(title="立即登录" rightIcon="keyboard_arrow_right" @click="$router.push({ name: 'login' })")
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  methods: {
    ...mapActions('auth', [
      'logout'
    ])
  },
  computed: {
    ...mapGetters('auth', [
      'isLogin',
      'userName'
    ]),
    avatarPath () {
      return this.isLogin ? '/setting/' : '/login/'
    }
  }
}
</script>

<style lang="stylus">
.top
  background-color teal
  display flex
  justify-content center
  padding-top 3em
  padding-bottom 1.5em
.mine-avatar-center
  display flex
  flex-direction column
  justify-content space-between
  align-items center
.mine-avatar-button
  padding-top 0.5em
.mine-paper
  display flex
  justify-content center
  align-items center
  .mine-icon
    font-size 80px
    color #455a64
.mine-menu
  overflow auto
</style>
