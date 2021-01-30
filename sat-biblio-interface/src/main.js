import Vue from 'vue'
import App from './App.vue'
import { BootstrapVue } from 'bootstrap-vue'
// Import Bootstrap an BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import axios from "axios";
import VueTypeaheadBootstrap from 'vue-typeahead-bootstrap'
import router from "./router";
Vue.config.productionTip = false

Vue.use(BootstrapVue)
import store from "./store";

Vue.component('vue-typeahead-bootstrap', VueTypeaheadBootstrap)
axios.defaults.baseURL = "http://localhost:5000";
axios.defaults.withCredentials = true;

new Vue({
  render: h => h(App),
  router,
  store
}).$mount('#app')
