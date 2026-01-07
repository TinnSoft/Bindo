/* Minimal Quasar Vite config for dev server */
const { configure } = require('quasar/wrappers')

module.exports = configure(function () {
  return {
    eslint: {
      warnings: false,
      errors: false
    },
    devServer: {
      port: 8080,
      open: false
    },
    framework: {
      config: {}
    }
  }
})
