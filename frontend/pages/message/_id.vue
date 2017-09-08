<template lang="pug">
.detail
  mu-appbar(title="消息详情")
    nuxt-link.nuxt-link-active(to="/" slot="left")
      mu-icon-button(icon="navigate_before")
  mu-list.message-detail
    mu-list-item(:title="message.doctor.title")
      mu-avatar(v-if="message.doctor.image", :src="`/${message.doctor.image}`" slot="leftAvatar")
      i(v-else class="material-icons mine-icon" slot="leftAvatar") face
      span.message(slot="describe")
        span(style="color: rgba(0, 0, 0, .87)") {{ `${message.doctor.name}` }}
        br
        template {{ `${message.doctor.team} | ${message.doctor.job} | ${utils.classifyDisplay(message.doctor.classify)}` }}
  mu-divider
  mu-content-block.message-content
    .time-center {{ utils.classifyDisplay(message.create_time) }}
    hgroup.speech-bubble.right
      h2 {{ message.title }}
    hgroup.speech-bubble.right(v-if="message.detail.length > 0")
      h2 {{ message.detail }}
</template>

<script>
export default {
  async asyncData ({ app, params }) {
    let data = await app.$axios.$get(`/care/message/${params.id}/`)
    return { message: data }
  },
  data () {
    return {
      message: []
    }
  },
  methods: {
    timeDisplay (time) {
      return this.$moment(time, this.$moment.ISO_8601).fromNow()
    }
  },
  computed: {
  }
}
</script>

<style lang="stylus">
.message-time
  font-size 12px
  color #bdbdbd
  display inline
.message-detail
  background-color #eceff1
  padding 0
  .mu-item
    padding 8px 8px 8px 72px
.speech-bubble
	position relative
	background #009688
	border-radius .4em
  padding .4em
  max-width 80vw
.speech-bubble:after .right
	content ''
	position absolute
	top 50%
	width 0
	height 0
	border 0.625em solid transparent
	border-top 0
	margin-top -0.312em
  right 0
  border-left-color #009688
	border-right 0
  margin-right -0.625em
.speech-bubble:after .left
  content ''
	position absolute
	top 50%
	width 0
	height 0
	border 0.625em solid transparent
	border-top 0
	margin-top -0.312em
  left 0
  border-right-color #009688
	border-left 0
  margin-left -0.625em
</style>
