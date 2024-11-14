<template>
    <div>
        <!-- 遍历 history_search 数组 -->
        <div v-for="(search, index) in form.history_search" :key="index">
            <!-- 展示每个搜索记录的详细信息 -->
            <p>搜索ID: {{ search.search_id }}</p>
            <p>搜索内容: {{ search.search_text }}</p>
            <p>商品ID列表:</p>
            <p>商品数量: {{ search.num_items }}</p>
        </div>
    </div>
</template>

<script setup>
import { useStore } from 'vuex'
import { reactive } from 'vue';
import { onMounted } from 'vue'

import { notify } from '@/composables/utils'
import { history } from '@/api/api';

const store = useStore()
const User = store.state.user;

const form = reactive({
    history_search: []
})

onMounted(() => {
    history(User.id)
        .then(res => {
            form.history_search = res.data
            notify('success', res.message)
        })
})

</script>