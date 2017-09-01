const webpack = require('webpack')

module.exports = {
  /*
  ** Headers of the page
  */
  head: {
    title: 'frontend',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'Nuxt.js project' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      // { rel: 'stylesheet', href: '//fonts.useso.com/css?family=Roboto:300,400,500,700,400italic' },
      { rel: 'stylesheet', href: 'http://cdn.bootcss.com/material-design-icons/3.0.1/iconfont/material-icons.css' }
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#3B8070' },
  /*
  ** Build configuration
  */
  plugins: [
    '~/plugins/mint-ui',
    '~/plugins/muse-ui',
    '~/plugins/url'
  ],
  build: {
    /*
    ** Run ESLINT on save
    */
    extend (config, ctx) {
      if (ctx.dev && ctx.isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/
        })
      }
    },
    vendor: [
      'axios',
      'mint-ui',
      'url',
      'vee-validate'
    ],
    plugins: [
      // '~/plugins/mint-ui',
      new webpack.ProvidePlugin({
        '_': 'lodash'
      })
    ]
  },
  modules: [
    '@nuxtjs/proxy'
  ],
  proxy: {
    '/api/**': 'http://127.0.0.1:8000'
  },
  css: [
    { src: '~assets/css/font.stylus', lang: 'stylus' }
  ]
}
