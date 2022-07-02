import { createStore} from "vuex";
import authModule from '@/store/modules/auth/index';
import stockModule from '@/store/modules/stock/index'

const store = createStore({
    modules: {
        auth: authModule,
        stock: stockModule
    },
});

export default store;