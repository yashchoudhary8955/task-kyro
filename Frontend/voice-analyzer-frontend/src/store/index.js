import { createStore } from 'vuex';
import createPersistedState from 'vuex-persistedstate';

const store = createStore({
  state: {
    token: null,
    user: null
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
    },
    setUser(state, user) {
      state.user = user;
    },
    logout(state) {
      state.token = null;
      state.user = null;
    }
  },
  actions: {
    setToken({ commit }, token) {
      commit('setToken', token);
    },
    setUser({ commit }, user) {
      commit('setUser', user);
    },
    logout({ commit }) {
      commit('logout');
    }
  },
  plugins: [createPersistedState()]
});

export default store;
