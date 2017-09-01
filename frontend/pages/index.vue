<template lang="pug">
main
  .page-tab-container
    mt-tab-container(v-model="selected" swipeable)
      mt-tab-container-item(id="index")
        mt-cell(v-for="n in 10" title="tab-container 1", :key="n")
      mt-tab-container-item(id="mine")
        Mine
  .nav
    mt-tabbar(v-model="selected", :fixed="true")
      mt-tab-item(id="index")
        img(slot="icon")
        template 首页
      mt-tab-item(id="mine")
        img(slot="icon")
        template 我的
</template>

<script>
import Logo from '~/components/Logo.vue'
import Mine from '~/components/mine/index.vue'

export default {
  components: {
    Logo,
    Mine
  },
  data () {
    return {
      selected: 'mine'
    }
  }
}
</script>

<style lang="stylus">
.item
  display inline-block
.link
  color inherit
  padding 20px
  display block
</style>
