import Vuex from "vuex";
import Vue from "vue";

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        connected: false,
        right: 1,
        connectionInfo: {}
    },
    mutations: {
        connect(state, payload) {
            state.connected = true;
            state.right = payload.right;
            state.connectionInfo = payload.connectionInfo;
        },
        disconnect(state) {
            state.connected = false;
            state.right = 1;
            state.connectionInfo = {};
        },
    }
});

export default store;