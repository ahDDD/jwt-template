<template lang="pug">
mu-content-block.care
  h1 身体小问题, 快速找医生
  mu-raised-button.login-button(label="找医生" fullWidth primary @click="$router.push({ name: 'care-classify' })")
  footer
    img(src="~static/main_logo.png")
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  methods: {
  },
  computed: {
    ...mapGetters([
      'isLogin',
      'userName',
      'user'
    ])
  }
}
</script>

<style lang="stylus">
.care
  footer
    height 74vh
    display flex
    justify-content center
    align-items flex-end
    img
      height 2em
  h1
    color #78909c
    text-align center
</style>
