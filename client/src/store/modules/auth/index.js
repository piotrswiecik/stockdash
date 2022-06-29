/*
Auth module for vuex.
Handles all security on frontend.

Authentication workflow:

 */

import getters from "@/store/modules/auth/getters";
import actions from '@/store/modules/auth/actions';
import mutations from '@/store/modules/auth/mutations';

export default {
    state() {
        return {
            userIsAuthenticated: false,
            authToken: null,
            refreshToken: null,
            userId: null,
            username: null,
            isAdmin: false,
        };
    },
    namespaced: true,
    getters: getters,
    actions: actions,
    mutations: mutations,
};