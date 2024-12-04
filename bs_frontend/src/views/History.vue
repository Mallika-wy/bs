<template>
    <div class="history_container" v-if="!itemsVisible">
        <el-row :gutter="20">
            <el-col :xs="24" :sm="12" :md="8" :lg="8" v-for="item in form.history_search" :key="item.search_id">
                <el-card>
                    <div style="margin-left: 10px; text-align: start; font-size: 16px;">
                        <p style="padding: 2.5px;"><span style="font-weight: bold;">搜索ID: </span>{{ item.search_id }}</p>
                        <p style="padding: 2.5px;"><span style="font-weight: bold;">搜索内容: </span>{{ item.search_text }}</p>
                        <p style="padding: 2.5px;"><span style="font-weight: bold;">商品数量: </span>{{ item.num_items }}</p>
                    </div>
                    <el-button type="primary" @click="viewItems(item)">查看商品</el-button>
                </el-card>
            </el-col>
        </el-row>
    </div>
    <el-scrollbar v-if="itemsVisible" height="100%" class="scrollbar">
        <div @click="closeItemsBoard" class="back-icon">
            <el-icon>
                <ArrowLeft />
            </el-icon>
            返回商品库
        </div>
        <div class="title">商品列表</div>
        <el-row :gutter="20">
            <el-col :xs="24" :sm="12" :md="8" :lg="8" v-for="item in form.item_list" :key="item.id">
                <el-card>
                    <div style="margin-left: 10px; text-align: start; font-size: 16px;">
                        <p style="padding: 2.5px;"><span style="font-weight: bold;">名称：</span>{{ item.title }}</p>
                        <p style="padding: 2.5px;">
                            <span style="font-weight: bold;">价格: </span>
                            <span v-if="item.price === -1">进入详情页查看价格</span>
                            <span v-else>{{ item.price }}</span>
                        </p>
                        <p style="padding: 2.5px;">
                            <span style="font-weight: bold;">平台：</span>
                            <span v-if="item.type === 1">淘宝</span>
                            <span v-else>京东</span>
                        </p>
                    </div>
                </el-card>
            </el-col>
        </el-row>
    </el-scrollbar>
</template>

<script setup>
import { useStore } from 'vuex'
import { reactive, ref } from 'vue';
import { onMounted } from 'vue'

import { notify } from '@/composables/utils'
import { history, getItemsFromSearchID } from '@/api/api';

const store = useStore()
const User = store.state.user;

const form = reactive({
    history_search: [],
    item_list: []
})
const itemsVisible = ref(false)

onMounted(() => {
    history(User.id)
        .then(res => {
            form.history_search = res.data
            notify('success', res.message)
        })
})

const viewItems = (row) => {
    getItemsFromSearchID(User.id, row.search_id)
        .then(res => {
            console.log(res)
            if (res.code === 200) {
                notify('success', res.message)
                console.log(res)
                form.item_list = res.data
                itemsVisible.value = true
            } else {
                notify('error', res.message)
            }
        })
};

const closeItemsBoard = () => {
    itemsVisible.value = false
    form.item_list = []

}
</script>

<style scope>
h2 {
    font-size: 24px;
    margin-bottom: 10px;
}

p {
    font-size: 16px;
    line-height: 2.0;
    margin-bottom: 10px;
}

strong {
    font-weight: bold;
}

.history_container {
  width: 100%;
  margin: 0 auto; /* 上下边距为0，左右自动（自动边距使容器居中） */
  padding: 20px; /* 内边距 */
}

.scrollbar {
    display: flex;
    align-items: center;
    height: 100%;
    margin: 10px;
    text-align: center;
    border-radius: 4px;
}

.search-container {
    display: flex;
    /* 使用flex布局 */
    align-items: center;
    /* 垂直居中 */
    gap: 18px;
    /* 元素之间的间距 */
}

.title {
    margin-top: 20px;
    /* margin-left: 20px; */
    font-size: 2em;
    /* 字体大小 */
    font-weight: 500;
    /* 字体权重，已调整为不那么粗 */
    color: #333;
    /* 文本颜色，可以根据需要调整 */
    text-align: left;
    /* 文本对齐方式 */
}

.back-icon {
    display: flex;
    align-items: center;
    cursor: pointer;
    color: #007bff;
    font-size: 16px;
    margin-bottom: 20px;
}
</style>