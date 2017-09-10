<template lang="pug">
  mu-dialog(:open="dialog.show", :title="dialog.title" @close="dialog.show = false")
    mu-text-field(
      v-if="dialog.transKey === 'age'"
      v-model="dialog.value"
      fullWidth
      required,
      type="number",
      :errorText="dialog.error",
      @focus="dialog.error = ''")
    mu-select-field(
      v-else-if="dialog.transKey === 'sex'"
      v-model="dialog.value",
      :labelFocusClass="['label-foucs']"
      label="性别",
      :errorText="dialog.error"
      fullWidth
      @open="dialog.error = ''")
      mu-menu-item(value="male" title="男")
      mu-menu-item(value="female" title="女")
      mu-menu-item(value="secret" title="保密")
    mu-text-field(
      v-else
      v-model="dialog.value"
      fullWidth
      required,
      :errorText="dialog.error",
      @focus="dialog.error = ''")
    mu-flat-button(slot="actions" @click="dialog.show = false" primary label="取消")
    mu-flat-button(slot="actions" primary @click="close" label="确定")
</template>

<script>
import isEmail from 'validator/lib/isEmail'

export default {
  props: {
    userInfo: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      dialog: {
        show: false,
        value: '',
        key: '',
        title: '',
        transKey: '',
        error: ''
      }
    }
  },
  methods: {
    validate () {
      this.dialog.error = this.dialog.value === '' ? '不能为空' : ''
      if (this.dialog.transKey === 'email') {
        this.dialog.error = isEmail(this.dialog.value) ? '' : '请输入合法邮箱'
      } else if (this.dialog.transKey === 'name') {
        this.dialog.error = this.dialog.value.length > 10 ? '过长了' : ''
      } else if (this.dialog.transKey === 'age') {
        this.dialog.error = this.dialog.value > 0 && this.dialog.value < 70 ? '' : '请输入真实年龄'
      }
    },
    openDialog (key) {
      this.dialog.title = key
      this.dialog.transKey = {
        '姓名': 'name',
        '性别': 'sex',
        '邮箱': 'email',
        '战队': 'team',
        '医院': 'team',
        '职位': 'job',
        '职称': 'job',
        '游戏': 'game',
        '年龄': 'age'
      }[key]
      this.dialog.value = this._.cloneDeep(this.userInfo[this.dialog.transKey])
      this.$nextTick(() => {
        this.dialog.show = true
      })
    },
    close () {
      this.validate()
      if (this.dialog.error === '') {
        this.userInfo[this.dialog.transKey] = this.dialog.value
        this.dialog.show = false
      }
    }
  }
}
</script>

<style lang="stylus">
</style>
