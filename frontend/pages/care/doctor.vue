<template lang="pug">
div
  mu-appbar(title="医生分类")
    nuxt-link(to="/" slot="left")
      mu-icon-button(icon="navigate_before" slot="left")
  mu-back-top(:height="1", :bottom="100", :right="50", :duration="1000", :callBack="backTopCallBack")
    mu-raised-button(label="Back Top" class="demo-raised-button" primary)
  .care-content
    mu-list
      mu-list-item(
        v-for="(item, index) in classifyList",
        :key="index",
        :title="item[1]",
        :describeText="item[2]"
        @click="openPopup(item)")
        mu-icon(value="keyboard_arrow_right" slot="right")
  mu-popup(position="right" popupClass="popup-right", :open="popup.show" @close="closePopup")
    mu-appbar(:title="popup.title")
      mu-flat-button(slot="right" label="关闭" color="white" @click="closePopup")
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  async asyncData ({ app }) {
    let data = await app.$axios.$get('/care/get_classify_detail/')
    return { classifyList: data.classify }
  },
  data () {
    return {
      classifyList: [],
      popup: {
        show: false,
        title: '',
        detail: '',
        key: ''
      }
    }
  },
  methods: {
    ...mapActions([
      'logout'
    ]),
    backTopCallBack () {
      window.alert('I back top!')
    },
    openPopup (data) {
      this.popup.key = data[0]
      this.popup.title = data[1]
      this.popup.detail = data[2]
      this.popup.show = true
    },
    closePopup () {
      this.popup.show = false
    }
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
.care-content
  height 90vh
  overflow scroll
::-webkit-scrollbar
	width 8px /*滚动条的宽度*/
	height 8px /*滚动条的高度*/
.popup-right
  display flex
  width 100%
  height 100%
  max-width 100vw
  align-items center
  padding 24px
</style>
