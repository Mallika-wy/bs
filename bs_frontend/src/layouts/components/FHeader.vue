<template>
    <div class="f-header">
        <span class="logo">
            <el-icon>
                <eleme-filled />
            </el-icon>
            ZJU B/S 商品比价网站
        </span>
        <el-icon class="icon-btn" title="退出登录" @click="logout">
            <Fold />
        </el-icon>
    </div>
</template>

<script setup>
import { useStore } from 'vuex';
import { useRouter } from 'vue-router'
import { notify } from '@/composables/utils'
import { removeToken } from '@/composables/cookie'
const store = useStore();
const router = useRouter()
const logout = () => {
    store.commit('setUser', null)
    removeToken()
    router.push('/login')
    notify('info', '退出登录')
}
</script>

<style>
.f-header {
    @apply flex items-center bg-indigo-700 text-light-50 fixed top-0 left-0 right-0;
    height: 80px;
    z-index: 1;
}

.logo {
    width: 250px;
    @apply flex justify-center items-center text-xl font-thin;
}

.icon-btn {
    @apply flex justify-center items-center;
    width: 42px;
    height: 80px;
    cursor: pointer;
    margin-left: auto; /* 自动推到右侧 */
}

.icon-btn:hover {
    @apply bg-indigo-600;
}

</style>