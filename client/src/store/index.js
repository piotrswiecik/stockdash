import { createStore} from "vuex";

const store = createStore({
   state() {
       return {
        test: 666,
       };
   }
});

export default store;