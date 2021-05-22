import Vuex from "vuex";
import Vue from "vue";
import {isValidJwt} from "@/services/authentication";
import localStorageManager from "@/services/localstorageManager";

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        connected: false,
        connectionInfo: {}
    },
    mutations: {
        initialiseStore(state) {
            console.log("initialiseStore");
            const sessionInfo = localStorageManager.getSessionInfo();
            console.log("token");
            console.log(isValidJwt(sessionInfo.token));
            if(sessionInfo &&
                sessionInfo.token
                && isValidJwt(sessionInfo.token)) {
                state.connected = true;
                // state.right = sessionInfo.right;
                state.connectionInfo = sessionInfo;
                // state.token = sessionInfo.token;

            } else {
                console.log("disconnected");
                state.connected = false;
                // state.right = 1;
                state.connectionInfo = {};
                // state.token = '';
            }
        },
        connect(state, payload) {
            state.connected = true;
            state.connectionInfo = payload.connectionInfo;
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
        },
        getUserRight(state) {
            return state.connectionInfo.right;
        },
        getConnectionInfo(state) {
            return state.connectionInfo;
        }
    }
});

export default store;