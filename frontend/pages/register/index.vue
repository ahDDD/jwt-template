<template lang="pug">
.register
  mt-header(title="注册")
    nuxt-link(to="/" slot="left")
      mt-button(icon="back")
  nuxt-link(to="/register/doctor/")
    mt-button(type="primary") 医生
  nuxt-link(to="/register/player/")
    mt-button(type="default") 玩家
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

</style>
