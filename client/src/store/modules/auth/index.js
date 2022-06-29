/*
Auth module for vuex.
Handles all security on frontend.

Authentication workflow:
-> All routes are protected - except '/login'
-> When protected route is accessed, vue-router navguard checks for auth status (getters -> 'auth/userIsAuthenticated')
-> userIsAuthenticated getter is defined as 'token not null && userId not null'
-> If not auth, user is redirected to /login. Else - requested route is served normally.
-> On login form submit, fields are validated & if ok - login method in LoginForm component is called async
-> login method dispatches 'auth/loginRequest' action with username and password payload -> await loginResponse
-> loginRequest queries backend for JWT token via REST endpoint
-> If loginRequest failed, throw error & handle it in LoginForm (display error box)
-> If loginRequest ok, commit setAuthenticatedStatus mutation to set all token data in vuex state
-> after login, replace routerview with main page
-> REST provides two tokens - main and refresh - as per JWT-Extended specs
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