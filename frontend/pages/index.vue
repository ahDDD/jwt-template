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
        mu-bottom-nav-item(
          v-for="(item, index) in nav",
          :value="item.value",
          :title="item.title",
          :icon="item.icon",
          :key="index")
</template>

<script>
import { mapGetters } from 'vuex'
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
  },
  computed: {
    ...mapGetters([
      'user'
    ]),
    nav () {
      const nav = [
        { value: 'message', title: '消息', icon: 'message' },
        { value: 'mine', title: '我的', icon: 'account_circle' }
      ]
      if (this.user.user_type !== 'doctor') {
        nav.unshift({ value: 'care', title: '首页', icon: 'home' })
        return nav
      } else {
        return nav
      }
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
