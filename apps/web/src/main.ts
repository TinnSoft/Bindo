import { createApp } from 'vue'
import { Quasar } from 'quasar'
import App from './App.vue'
import router from './router'
import 'quasar/dist/quasar.css'
import axios from 'axios'

// i18n
import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import es from './locales/es.json'

// Use localhost:8000 in dev, api:8000 in docker
const isDev = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
axios.defaults.baseURL = isDev ? 'http://localhost:8000' : 'http://api:8000'

const i18n = createI18n({
  legacy: true,
  globalInjection: true,
  locale: 'es',
  fallbackLocale: 'en',
  messages: { en, es }
})

const app = createApp(App)
app.use(Quasar)
app.use(router)
app.use(i18n)
app.mount('#app')
