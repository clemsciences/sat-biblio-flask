import { createApp } from 'vue'
import App from './App.vue'
// import {BModal, BButton, BCol, BCard, BNav, BNavItem, BNavbar, BNavbarNav, BNavbarToggle, BContainer, BBadge, BAccordion,
//     BNavItemDropdown, BDropdown, BDropdownItem, BDropdownItemButton,
// BCollapse, BNavbarBrand, BForm, BFormGroup, BFormInput, BFormFile, BFormRadio, BFormRow, BFormCheckbox, BFormRadioGroup, BFormSelect, BFormCheckboxGroup,
// BRow, BListGroup, BListGroupItem, BPagination, BTooltip, BTable, BImg, BDropdownGroup
// } from 'bootstrap-vue-next'

import {createBootstrap} from 'bootstrap-vue-next/plugins/createBootstrap'
// import {BApp} from 'bootstrap-vue-next'
// import BootstrapVueNext from 'bootstrap-vue-next'
// Import Bootstrap and BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'
import 'bootstrap-icons/font/bootstrap-icons.css'  // ← Ajouter cette ligne

import Vue3BootstrapTypeahead from 'vue3-bootstrap-typeahead'
import router from "./router";
import store from "./store";
import { createHead } from '@vueuse/head'
import VueJsonPretty from 'vue-json-pretty'
import 'vue-json-pretty/lib/styles.css'
import { VueDatePicker } from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'

const app = createApp(App)
const head = createHead()

app.use(createBootstrap()) // Important
// app.use(BootstrapVueNext)  // Enregistrement du plugin
app.use(router)
app.use(store)
app.use(head)

// app.component('BButton', BButton);
// app.component('BModal', BModal);
// app.component('BCol', BCol);
// app.component('BCard', BCard);
// app.component('BNav', BNav);
// app.component('BNavItem', BNavItem);
// app.component('BNavbar', BNavbar);
// app.component('BContainer', BContainer);
// app.component('BAccordion', BAccordion);
// app.component('BBadge', BBadge);
// app.component('BNavItemDropdown', BNavItemDropdown);
// app.component('BDropdown', BDropdown);
// app.component('BDropdownItem', BDropdownItem);
// app.component('BDropdownItemButton', BDropdownItemButton);
// app.component('BNavbarToggle', BNavbarToggle);
// app.component('BNavbarNav', BNavbarNav);
// app.component('BCollapse', BCollapse);
// app.component('BNavbarBrand', BNavbarBrand);
// app.component('BForm', BForm);
// app.component('BFormGroup', BFormGroup);
// app.component('BFormInput', BFormInput);
// app.component('BFormFile', BFormFile);
// app.component('BFormRadio', BFormRadio);
// app.component('BFormRow', BFormRow);
// app.component('BFormCheckbox', BFormCheckbox);
// app.component('BFormRadioGroup', BFormRadioGroup);
// app.component('BFormSelect', BFormSelect);
// app.component('BFormCheckboxGroup', BFormCheckboxGroup);
// app.component('BRow', BRow);
// app.component('BListGroup', BListGroup);
// app.component('BListGroupItem', BListGroupItem);
// app.component('BPagination', BPagination);
// app.component('BTooltip', BTooltip);
// app.component('BTable', BTable);
// app.component('BImg', BImg);
// app.component('BDropdownGroup', BDropdownGroup);

app.component('VueDatePicker', VueDatePicker)
app.component('vue-typeahead-bootstrap', Vue3BootstrapTypeahead)
app.component("vue-json-pretty", VueJsonPretty)

store.commit('initialiseStore')

app.mount('#app')
