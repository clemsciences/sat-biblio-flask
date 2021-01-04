import Vue from 'vue'
import App from './App.vue'
import { BootstrapVue } from 'bootstrap-vue'
// Import Bootstrap an BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import router from "@/router";
import axios from "axios";
import VueBootstrapTypeahead from 'vue-bootstrap-typeahead'

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.component('vue-bootstrap-typeahead', VueBootstrapTypeahead)

axios.defaults.baseURL = "http://localhost:5000";

new Vue({
  render: h => h(App),
  router
}).$mount('#app')
