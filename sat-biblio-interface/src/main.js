import Vue from 'vue'
import App from './App.vue'
import {BootstrapVue, BootstrapVueIcons} from 'bootstrap-vue'
// Import Bootstrap and BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import VueTypeaheadBootstrap from 'vue-typeahead-bootstrap'
import router from "./router";
Vue.config.productionTip = false

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
import store from "./store";

Vue.component('vue-typeahead-bootstrap', VueTypeaheadBootstrap)


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
