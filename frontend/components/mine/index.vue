<template lang="pug">
div
  .top
    nuxt-link.mine-avatar-center(:to="avatarPath")
      mu-paper(class="mine-paper" circle :zDepth="4")
        mu-avatar(v-if="user.image", :src="`/${user.image}`", :size="80")
        i(v-else class="material-icons mine-icon") face
      mu-flat-button.mine-avatar-button(:label="`你好, ${userName}`" color="white")
      template(v-if="user.user_type")
        span(v-if="user.user_type === 'doctor'").main-span {{ `${user.team} | ${user.job} | ${user.classify}` }}
        span(v-else-if="user.user_type === 'player'").main-span {{ `${user.team} | ${user.job}` }}
  .settings
    mu-content-block
      mu-menu.mine-menu(:autoWidth="false", width="auto")
        template(v-if="isLogin")
          template(v-if="user.user_type === 'doctor'")
            mu-menu-item(
              :title="`${doctorProfileTitle}医生资料`"
              rightIcon="keyboard_arrow_right"
              @click="$router.push({ name: 'setting-profile' })")
          mu-menu-item(title="修改个人资料" rightIcon="keyboard_arrow_right" @click="$router.push({ name: 'setting' })")
          mu-menu-item(title="修改密码" rightIcon="keyboard_arrow_right" @click="$router.push({ name: 'setting-password' })")
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
    ...mapActions([
      'logout'
    ])
  },
  computed: {
    ...mapGetters([
      'isLogin',
      'userName',
      'user'
    ]),
    avatarPath () {
      return this.isLogin ? '/setting/' : '/login/'
    },
    doctorProfileTitle () {
      return this.user.user_type === 'doctor' ? (this.user.img === null && this.user.classify === '' ? '补充' : '修改') : ''
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
  border solid 2px #FFFFFF
  border-radius 40px
  background-color #FFFFFF
  .mine-icon
    font-size 80px
    color #455a64
.mine-menu
  overflow auto
.main-span
  color white
</style>
