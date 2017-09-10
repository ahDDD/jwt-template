<template lang="pug">
main
  .page-tab-container
    mt-tab-container(v-model="nav.selected" swipeable)
      mt-tab-container-item(id="care")
        Care(v-if="nav.selected === 'care'")
      mt-tab-container-item(id="message")
        Message(v-if="nav.selected === 'message'")
      mt-tab-container-item(id="mine")
        Mine(v-if="nav.selected === 'mine'")
  .nav
    mu-paper
      mu-bottom-nav(:value="nav.selected" @change="handleChange")
        mu-bottom-nav-item(
          v-for="(item, index) in nav.item",
          :value="item.value",
          :title="item.title",
          :icon="item.icon",
          :key="index")
</template>

<script>
import { mapMutations, mapGetters } from 'vuex'
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
    ...mapMutations([
      'SELECT_NAV'
    ]),
    handleChange (val) {
      this.SELECT_NAV(val)
    }
  },
  computed: {
    ...mapGetters([
      'user',
      'nav'
    ])
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
