import Vue from 'vue'
import App from './App.vue'
import { BootstrapVue } from 'bootstrap-vue'

Vue.config.productionTip = false

// Import Bootstrap an BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import router from "@/router";

Vue.use(BootstrapVue)

new Vue({
  render: h => h(App),
  router
}).$mount('#app')
