import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "@/pages/LoginPage";
import DashboardPage from "@/pages/DashboardPage";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            name: 'login',
            path: '/',
            component: LoginPage
        },
        {
            name: 'dashboard',
            path: '/dash',
            component: DashboardPage,
        }
    ],
});

export default router;