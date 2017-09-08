<template lang="pug">
main
  .page-tab-container
    mt-tab-container(v-model="selected" swipeable)
      mt-tab-container-item(id="care")
        Care(v-if="selected === 'care'")
      mt-tab-container-item(id="message")
        Message(v-if="selected === 'message'")
      mt-tab-container-item(id="mine")
        Mine(v-if="selected === 'mine'")
  .nav
    mu-paper
      mu-bottom-nav(:value="selected" @change="handleChange")
        mu-bottom-nav-item(value="care" title="首页" icon="home")
        mu-bottom-nav-item(value="message" title="消息" icon="message")
        mu-bottom-nav-item(value="mine" title="我的" icon="account_circle")
</template>

<script>
import Logo from '~/components/Logo.vue'
import Mine from '~/components/mine/index.vue'
import Care from '~/components/care/index.vue'
import Message from '~/components/message/index.vue'

export default {
  components: {
    Logo,
    Mine,
    Care,
    Message
  },
  data () {
    return {
      selected: 'mine'
    }
  },
  methods: {
    handleChange (val) {
      this.selected = val
    }
  }
}
</script>

<style lang="stylus">
main
  display flex
  min-height 100vh
  flex-direction column
.page-tab-container
  flex 1
.item
  display inline-block
.link
  color inherit
  padding 20px
  display block
</style>
