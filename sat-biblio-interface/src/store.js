import Vuex from "vuex";
import Vue from "vue";

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        connected: false,
        connectionInfo: {}
    },
    mutations: {
        connect(state, payload) {
            state.connected = true;
            state.connectionInfo = payload.connectionInfo;
        },
        disconnect(state) {
            state.connected = false;
            state.connectionInfo = {};
        },
    }
});

export default store;