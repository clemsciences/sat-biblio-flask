import Vuex from "vuex";
import Vue from "vue";
import createPersistedState from "vuex-persistedstate";
import {isValidJwt} from "@/services/authentication";
import {rights} from "@/services/rights";

Vue.use(Vuex)

const store = new Vuex.Store({
    plugins: [createPersistedState()],
    state: {
        connected: false,
        connectionInfo: {}
    },
    mutations: {
        initialiseStore(state) {
            if(state.connectionInfo &&
                state.connectionInfo.token &&
                isValidJwt(state.connectionInfo.token)) {
                state.connected = true;
            } else {
                state.connected = false;
                state.connectionInfo = {};
            }
        },
        connect(state, payload) {
            state.connected = true;
            state.connectionInfo = payload.connectionInfo;
        },
        disconnect(state) {
            state.connected = false;
            state.connectionInfo = {};
        },
    },
    getters: {
        isAuthenticated(state) {
            if(state.connectionInfo) {
                return isValidJwt(state.connectionInfo.token);
            } else {
                return false;
            }
        },
        getUserRight(state) {
            if(state.connectionInfo) {
                return state.connectionInfo.right;
            } else {
                return rights.lecteur;
            }
        },
        isAdmin(state, getters) {
          return getters.getUserRight === rights.administrateur.index;
        },
        getConnectionInfo(state) {
            return state.connectionInfo;
        }
    }
});

export default store;