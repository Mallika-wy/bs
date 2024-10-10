import {
    createRouter,
    createWebHistory
} from 'vue-router'

import Layout from '@/layouts/Layout.vue'
import Login from "@/views/Login.vue"
import Register from "@/views/Register.vue"
import History from "@/views/History.vue"
import Search from "@/views/Search.vue"
import User from "@/views/User.vue"
import Item from "@/views/Item.vue"
import Document from "@/views/Document.vue"
import NotFount from "@/views/404.vue"

const routes = [
    {
        path: '/',
        component: Layout,
        redirect: '/document',
        children: [
            {
                path: '/document',
                component: Document,
                meta: {
                    title: '说明-ZJU B/S'
                }
            }, {
                path: '/history',
                component: History,
                meta: {
                    title: '商品库-ZJU B/S'
                }
            }, {
                path: '/search',
                component: Search,
                meta: {
                    title: '搜索-ZJU B/S'
                }
            }, {
                path: '/user',
                component: User,
                meta: {
                    title: '个人中心-ZJU B/S'
                }
            }]
    },
    {
        path: '/login',
        component: Login,
        meta: {
            title: '登录-ZJU B/S'
        }
    }, {
        path: '/register',
        component: Register,
        meta: {
            title: '注册-ZJU B/S'
        }
    }, {
        path: '/item',
        component: Item,
        meta: {
            title: '商品详情-ZJU B/S'
        }
    }, {
        path: '/:pathMatch(.*)',
        name: 'NotFound',
        component: NotFount
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router