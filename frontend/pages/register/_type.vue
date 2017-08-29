<template lang="pug">
.register
  mt-header(title="注册")
    nuxt-link(to="/register/" slot="left")
      mt-button(icon="back")
  .register
    mt-field(label="用户名" placeholder="请输入手机号" v-model="formData.phone")
    mt-field(label="密码" placeholder="请输入密码" type="password" v-modal="formData.password")
    mt-field(label="姓名" placeholder="请输入姓名" v-modal="formData.name")
    mt-field(label="性别" placeholder="请输入性别" v-modal="formData.sex")
    mt-field(:label="teamLabel" :placeholder="`请输入${teamLabel}`" v-modal="formData.team")
    mt-field(:label="jobLabel" :placeholder="`请输入${jobLabel}`" v-modal="formData.job")
    mt-button(size="large") 注册
</template>

<script>
export default {
  created () {
    const type = this.$route.params.type
    this.renderField(type)
    this.formData.user_type = type
  },
  data () {
    return {
      formData: {
        user_type: '',
        phone: '',
        password: '',
        name: '',
        sex: '',
        team: '',
        game: '',
        job: '',
        email: ''
      },
      teamLabel: '',
      jobLabel: ''
    }
  },
  methods: {
    handleClose () {},
    renderField (type) {
      this.teamLabel = type === 'doctor' ? '医院' : '战队'
      this.jobLabel = type === 'doctor' ? '职位' : '职业'
    }
  },
  computed: {
  }
}
</script>

<style lang="stylus">

</style>
