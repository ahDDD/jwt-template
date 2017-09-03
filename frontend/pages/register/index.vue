<template lang="pug">
.register
  mu-appbar(title="注册")
    nuxt-link.nuxt-link-active(to="/login/" slot="left")
      mu-icon-button(icon="navigate_before")
  mu-content-block.register-content.type
    nuxt-link(to="/register/doctor/").type-button
      mu-raised-button(label="医生" fullWidth primary)
    nuxt-link(to="/register/player/").type-button
      mu-raised-button(label="玩家" primary fullWidth)
    nuxt-link(to="/register/normal/").type-button
      mu-raised-button(label="普通用户" primary fullWidth)
</template>

<script>
export default {
  data () {
    return {
    }
  },
  methods: {
  },
  computed: {
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
</style>
