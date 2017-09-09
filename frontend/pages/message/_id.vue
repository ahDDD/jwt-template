<template lang="pug">
.message
  mu-appbar(title="消息详情")
    nuxt-link.nuxt-link-active(to="/" slot="left")
      mu-icon-button(icon="navigate_before")
  mu-linear-progress(v-if="loading")
  .message-main
    mu-list.message-detail-doctor(v-if="type === 'user'")
      mu-list-item(:title="message.doctor.title")
        mu-avatar(v-if="message.doctor.image", :src="`/${message.doctor.image}`" slot="leftAvatar")
        i(v-else class="material-icons mine-icon" slot="leftAvatar") face
        span(slot="describe")
          span(style="color: rgba(0, 0, 0, .87)") {{ `${message.doctor.name}` }}
          br
          template {{ `${message.doctor.team} | ${message.doctor.job} | ${utils.classifyDisplay(message.doctor.classify)}` }}
    mu-list.message-detail-user(v-else)
      mu-sub-header 患者信息:
      .left
        mu-list-item(disabled, :title="message.user.name", :describeText="`${message.user.age}岁 | ${utils.sexDisplay(message.user.sex)}`")
    mu-divider
    mu-content-block.message-content
      .time-center {{ timeDisplay(message.create_time) }}
      .message-right
        hgroup.speech-bubble-right
          p {{ message.title }}
        hgroup.speech-bubble-right(v-if="message.detail.length > 0")
          p {{ message.detail }}
      template(v-for="(item, index) in message.comment")
        .time-center {{ timeDisplay(item.create_time) }}
        .message-left
          hgroup.speech-bubble-left
            p {{ item.content }}
  mu-content-block.message-footer(v-if="type === 'doctor'")
    mu-text-field(
      labelFloat
      hintText="",
      hintTextClass="post-hint-text"
      v-model="formData.content",
      :errorText="error.content"
      fullWidth
      @focus="error.content = ''"
      multiLine,
      :rows="1",
      :rowsMax="2")
    mu-raised-button(label="回复" @click="comment" primary)
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  async asyncData ({ app, params }) {
    const data = await app.$axios.$get(`/care/message/${params.id}/`)
    const type = data.doctor ? 'user' : 'doctor'
    return { message: data, type: type }
  },
  data () {
    return {
      message: [],
      type: '',
      formData: {
        content: ''
      },
      error: {
        content: ''
      },
      snackbar: {
        show: false,
        message: '',
        time: ''
      },
      loading: false
    }
  },
  methods: {
    timeDisplay (time) {
      return this.$moment(time, this.$moment.ISO_8601).fromNow()
    },
    validate () {
      this.error.content = this.formData.content ? '' : '不能为空'
    },
    isValidate () {
      return Object.values(this.error).every(x => x === '')
    },
    async comment () {
      this.validate()
      if (this.isValidate()) {
        this.loading = true
        try {
          this.formData.user = this.user.id
          this.formData.post = this.message.id
          const data = await this.$axios.$post(this.url.COMMENT, this.formData)
          this.loading = false
          this.message.comment.push(data)
          this.formData.content = ''
          // this.showSnackbar('回复成功')
          // setTimeout(() => { this.$router.push({ name: 'index' }) }, 1500)
        } catch (error) {
          const data = error.response.data
          const message = [].concat.apply([], Object.values(data)).join(',')
          this.loading = false
          this.showSnackbar(`回复失败: ${message}`)
        }
      } else {
        this.showSnackbar('输入有误, 请重新输入')
      }
    },
    showSnackbar (message) {
      this.snackbar.message = message
      this.snackbar.show = true
      if (this.snackbar.time) clearTimeout(this.snackbar.time)
      this.snackbar.time = setTimeout(() => { this.snackbar.show = false }, 2500)
    },
    hideSnackbar () {
      this.snackbar.show = false
      if (this.snackbar.time) clearTimeout(this.snackbar.time)
    },
    handleInputOverflow (isOverflow) {
      this.error.title = isOverflow ? '超长了' : ''
    }
  },
  computed: {
    ...mapGetters([
      'user'
    ])
  }
}
</script>

<style lang="stylus">
.message
  display flex
  min-height 100vh
  flex-direction column
.message-time
  font-size 12px
  color #bdbdbd
  display inline
.message-detail-doctor
  background-color #eceff1
  padding 0
  .mu-item
    padding-top 8px
    padding-right 8px
    padding-bottom 8px
.message-detail-user
  background-color #eceff1
  padding 0
  .left
    display flex
    justify-content flex-end
  .mu-item
    padding 4px 16px
  div.mu-sub-header:first-child
    margin-top 4px
    line-height 30px
.message-detail-user .mu-item-title
  text-align right
  font-size 22px
.time-center
  display flex
  justify-content center
  color #9e9e9e
  margin-bottom .5em
hgroup
  padding .4em
  // max-width 80vw
  margin-bottom .5em
  width auto
.message-right
  display flex
  flex-direction column
  justify-content space-between
  align-items flex-end
  color white
.speech-bubble-right
	position relative
	background #009688
	border-radius .4em
.speech-bubble-right:after
	content ''
	position absolute
	right 0
	top 50%
	width 0
	height 0
	border .5em solid transparent
	border-left-color #009688
	border-right 0
	border-top 0
	margin-top -0.187em
	margin-right -0.5em
.message-left
  display flex
  color black
.speech-bubble-left
	position relative
	background #eceff1
	border-radius .4em
.speech-bubble-left:after
	content ''
	position absolute
	left 0
	top 50%
	width 0
	height 0
	border 0.625em solid transparent
	border-right-color #eceff1
	border-left 0
	border-bottom 0
	margin-top -0.312em
	margin-left -0.625em
.message-main
  flex 1
.message-content
  height 70vh
  overflow auto
.message-footer
  display grid
  grid-template-columns 3fr 1fr
  grid-column-gap 10px
  padding-bottom 0
  padding-top 0
</style>
