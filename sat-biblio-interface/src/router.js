

import Vue from "vue";
import VueRouter from "vue-router";
import Recherche from "@/components/Recherche";
import Accueil from "@/components/Accueil";
import Export from "@/components/Export";

Vue.use(VueRouter);

export default new VueRouter({
    mode: "history",
    routes: [
        {
            path: '/recherche',
            component: Recherche
        },
        {
            path: '',
            component: Accueil
        },
        {
            path: '/export',
            component: Export
        },
        {

        }
    ]

})