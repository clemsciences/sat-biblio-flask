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
axios.defaults.headers.post['Access-Control-Allow-Origin'] = 'https://satbiblio.clementbesnier.eu';

import VueMeta from 'vue-meta';
Vue.use(VueMeta);

import VueJsonPretty from 'vue-json-pretty';
Vue.component("vue-json-pretty", VueJsonPretty);

new Vue({
  render: h => h(App),
  router,
  store,
  beforeCreate() {
		this.$store.commit('initialiseStore');
	}
}).$mount('#app')
