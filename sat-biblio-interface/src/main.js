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
axios.defaults.baseURL = process.env.VUE_APP_SITE_API_URL;
axios.defaults.withCredentials = true;
axios.defaults.headers.post['Access-Control-Allow-Origin'] = 'https://api.satbiblio.clementbesnier.eu,https://satbiblio.clementbesnier';

new Vue({
  render: h => h(App),
  router,
  store,
  beforeCreate() {
		this.$store.commit('initialiseStore');
	}
}).$mount('#app')
