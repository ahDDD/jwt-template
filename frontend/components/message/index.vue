<template lang="pug">
.message
  mu-appbar(title="消息")
  mu-list
    mu-list-item(v-for="(item, index) in messageList", :title="item.title", :key="index")
      span.message(slot="describe")
        span(style="color: #90a4ae") {{ `向${item.doctor}问询` }}
        span.message-time {{ ` - 最后更新于 ${timeDisplay(item.update_time)}` }}
      mu-icon(value="chat" slot="right" @click="openDetail(item)")
</template>

<script>
export default {
  async mounted () {
    this.messageList = await this.$axios.$get('/care/post/list/')
  },
  data () {
    return {
      messageList: []
    }
  },
  methods: {
    timeDisplay (time) {
      return this.$moment(time, this.$moment.ISO_8601).fromNow()
    },
    openDetail (item) {
      this.$router.push({
        name: 'message-id',
        params: { id: item.id }
      })
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
</style>
