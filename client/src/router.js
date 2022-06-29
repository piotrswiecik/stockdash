import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "@/pages/LoginPage";
import DashboardPage from "@/pages/DashboardPage";
import store from "@/store";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { // protected by login
            name: 'dashboard',
            path: '/',
            component: DashboardPage,
        },
        {
            name: 'login',
            path: '/login',
            component: LoginPage,
        }
    ],
});

// eslint-disable-next-line no-unused-vars
router.beforeEach((to, from, next) => {
    // for all routes - if user is not logged in - redirect to login page
    if (to.name !== 'login' && !store.getters['auth/userIsAuthenticated']) {
        console.log('redir to login');
        next({name: 'login'});
    } else {
        next();
    }
})

export default router;