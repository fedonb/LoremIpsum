import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'
import Axios from 'axios'
import App from './App.vue'
import router from './router'
import store from './store'
import 'bootstrap/dist/css/bootstrap.css'
import 'vuetify/dist/vuetify.min.css'
import vuetify from '@/plugins/vuetify' // path to vuetify export

Vue.use(BootstrapVue)

Vue.prototype.$http = Axios

const token = localStorage.getItem('user-token')
if (token) {
  Vue.prototype.$http.defaults.headers.common.Authorization = token
}

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App)
}).$mount('#app')
