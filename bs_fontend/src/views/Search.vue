<template>
    <el-input v-model="form.search_text" placeholder="输入商品名称">
        <template #prefix>
            <el-icon>
                <Search />
            </el-icon>
        </template>
    </el-input>

    <el-button type="primary" @click="search">搜索</el-button>
</template>

<script setup>
import { reactive } from 'vue'
import { useStore } from 'vuex'

import { notify } from '@/composables/utils'
import { searchItem } from '@/api/api';

const store = useStore()
const User = store.state.user;

const form = reactive({
    search_text: ''
})

const search = () => {
    if (!form['search_text'].trim()) {
        notify('error', "搜索内容不能为空")
        return;
    }

    searchItem(User.id, form.search_text)
        .then(res => {
            if (res.code === 200) {
                notify('success', res.message)
                router.push('/SearchResult')
            } else {
                notify('error', res.message)
            }
        })
}
</script>