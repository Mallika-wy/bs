import { createStore } from "vuex"

const store = createStore({
  state() {
    return {
        user_id: {}
    }
  },
  mutations: {
    setUser(state, user_id) {
      state.user_id = user_id
    },
  }
})


export default store