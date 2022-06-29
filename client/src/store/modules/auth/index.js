import getters from "@/store/modules/auth/getters";
import actions from '@/store/modules/auth/actions';
import mutations from '@/store/modules/auth/mutations';

export default {
    state() {
        return {
            userIsAuthenticated: false,
        };
    },
    namespaced: true,
    getters: getters,
    actions: actions,
    mutations: mutations,
};