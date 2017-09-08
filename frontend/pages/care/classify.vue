<template lang="pug">
div
  mu-appbar(title="医生分类")
    nuxt-link.nuxt-link-active(to="/" slot="left")
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
  mu-popup(position="right" popupClass="popup-right", :open="popup.show" @close="closePopup" @show="")
    mu-appbar(:title="popup.title")
      mu-flat-button(slot="right" label="关闭" color="white" @click="closePopup")
    .classify-content
      mu-content-block.classify-popup
        p {{ popup.detail }}
        mu-divider
        .divider {{ `为您推荐以下${doctorList.length}位医生` }}
      .classify-popup-center(v-if="popup.loading")
        mu-circular-progress(:size="40")
      mu-list(v-else)
        mu-list-item(v-for="item in doctorList", :title="item.name", :key="item.id")
          mu-avatar(v-if="item.image", :src="`/${item.image}`" slot="leftAvatar")
          i(v-else class="material-icons mine-icon" slot="leftAvatar") face
          span(slot="describe")
            span(style="color: rgba(0, 0, 0, .87)") {{ item.team }}
            br
            template {{ `${item.job} | ${utils.classifyDisplay(item.classify)}` }}
          mu-icon(value="chat_bubble" slot="right" @click="openDialog(item)")
    mu-dialog(:open="dialog.show", :title="`向${dialog.title}提问`")
      mu-flat-button(slot="actions" @click="dialog.show = false" primary label="取消")
      mu-flat-button(slot="actions" @click="post" primary label="确定")
</template>

<script>
import { mapMutations, mapGetters } from 'vuex'

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
        key: '',
        loading: false
      },
      doctorList: [],
      dialog: {
        show: false,
        title: '',
        doctor: {}
      }
    }
  },
  methods: {
    ...mapMutations([
      'SET_DOCTOR'
    ]),
    backTopCallBack () {
      window.alert('I back top!')
    },
    openPopup (data) {
      this.popup.key = data[0]
      this.popup.title = data[1]
      this.popup.detail = data[2]
      this.popup.show = true
      this.fetchDoctor()
    },
    closePopup () {
      this.popup.show = false
    },
    async fetchDoctor () {
      this.popup.loading = true
      try {
        this.doctorList = await this.$axios.$get(`${this.url.DOCTOR}${this.popup.key}/`)
        this.popup.loading = false
      } catch (error) {
        const data = error.response.data
        const message = [].concat.apply([], Object.values(data)).join(',')
        this.popup.loading = false
        this.showSnackbar(`获取医生信息失败: ${message}`)
      }
    },
    openDialog (item) {
      this.dialog.title = item.name
      this.dialog.doctor = item
      this.$nextTick(() => {
        this.dialog.show = true
      })
    },
    post () {
      this.SET_DOCTOR(this.dialog.doctor)
      this.$router.push({ name: 'care-post' })
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
  width 100%
  height 100%
  max-width 100vw
.classify-popup
  background-color #eeeeee
  color #37474f
  p
    font-size 16px
  .divider
    padding 3px
    text-align center
.classify-popup-center
  display flex
  justify-content center
  align-items center
.classify-content
  height 90vh
  overflow auto
</style>
