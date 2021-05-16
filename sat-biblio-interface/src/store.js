import Vuex from "vuex";
import Vue from "vue";
import {isValidJwt} from "@/services/authentication";

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        token: '',
        connected: false,
        right: 1,
        connectionInfo: {}
    },
    mutations: {
        connect(state, payload) {
            state.connected = true;
            state.right = payload.right;
            state.connectionInfo = payload.connectionInfo;
            state.token = payload.token;
            localStorage.token = payload.token;
        },
        disconnect(state) {
            state.connected = false;
            state.connectionInfo = {};
            localStorageManager.removeSessionInfo();
        },
    },
    getters: {
        isAuthenticated(state) {
            return isValidJwt(state.token);
        }
    }
});

export default store;