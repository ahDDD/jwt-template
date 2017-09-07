<template lang="pug">
mu-content-block.care
  h1 身体小问题, 快速找医生
  mu-raised-button.login-button(label="找医生" fullWidth primary @click="$router.push({ name: 'care-classify' })")
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
    ])
  }
}
</script>

<style lang="stylus">
.care
  h1
    color #78909c
    text-align center
</style>
