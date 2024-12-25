<template>
    <el-scrollbar v-if="!dialogDetailVisible" height="100%" class="scrollbar">
        <div class="search-container">
            <el-input v-model="form.search_text" placeholder="输入商品名称">
                <template #prefix>
                    <el-icon>
                        <Search />
                    </el-icon>
                </template>
            </el-input>
            <el-button type="primary" @click="search">搜索</el-button>
        </div>

        <div class="title">商品列表</div>

        <el-row :gutter="20">
            <el-col :xs="24" :sm="12" :md="8" :lg="8" v-for="item in form.item_list" :key="item.id">
                <el-card>
                    <img :src="item.img_url" style="width: 100%; height: 250px; object-fit: cover;" />
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
                    <el-button type="primary" @click="showDetail(item)">查看详情</el-button>
                </el-card>
            </el-col>
        </el-row>
    </el-scrollbar>

    <div v-if="dialogDetailVisible">
        <div @click="closeDetail" class="back-icon">
            <el-icon>
                <ArrowLeft />
            </el-icon>
            返回搜索界面
        </div>

        <el-row class="containerdetail">
            <el-col :xs="24" :sm="12" :md="12" :lg="12">
                <img :src="form.detail.img_url" alt="商品图片"
                    style="width: 80%; height: auto; display: block; margin-bottom: 20px;" />
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12">
                <h2>{{ form.detail.title }}</h2>
                <p><strong>价格：</strong>{{ form.detail.price }}</p>
                <p><strong>商家昵称：</strong>{{ form.detail.nick }}</p>
                <p><strong>省份：</strong>{{ form.detail.procity }}</p>
                <p><strong>商品原链接：</strong><a :href="form.detail.item_url" target="_blank">{{ form.detail.item_url }}</a></p>
            </el-col>
        </el-row>
        <p><strong>历史价格查询：</strong><img :src="'data:image/png;base64,' + form.detail.history_image" alt="历史价格查询" /></p>
        <el-button @click="subscribe">降价通知</el-button>
    </div>

</template>

<script setup>
import { reactive, ref } from 'vue'
import { useStore } from 'vuex'

import { notify } from '@/composables/utils'
import { searchItems, searchItem, subscribeItem } from '@/api/api';

const store = useStore()
const User = store.state.user;

const dialogDetailVisible = ref(false)
const form = reactive({
    search_text: '',
    item_list: [],
    detail: {}
})

const search = () => {
    if (!form['search_text'].trim()) {
        notify('error', "搜索内容不能为空")
        return;
    }

    searchItems(User.id, form.search_text)
        .then(res => {
            if (res.code === 200) {
                notify('success', res.message)
                form.item_list = res.data
            } else {
                notify('error', res.message)
            }
        })
}

const showDetail = (item) => {
    searchItem(User.id, item.item_id)
        .then(res => {
            if (res.code === 200) {
                form.detail = res.data
                notify('success', res.message)
            } else {
                notify('error', res.message)
            }
        })
    dialogDetailVisible.value = true
}

const closeDetail = () => {
    dialogDetailVisible.value = false
    form.detail = {}
}

const subscribe = () => {
    subscribeItem(User.id, form.detail.id)
        .then(res => {
            if (res.code === 200) {
                notify('success', res.message)
            } else {
                notify('error', res.message)
            }
        })
}

</script>

<style scoped>
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

.containerdetail {
    padding: 20px; /* 内边距 */
    margin: 10 auto; /* 上下边距为0，左右自动（自动边距使容器居中） */
    background-color: #f9f9f9; /* 背景颜色 */
    border-radius: 8px; /* 圆角 */
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* 阴影 */
    max-width: 1200px; /* 最大宽度，根据需要调整 */
    width: 100%; /* 宽度100% */
}

/* 列样式 */
.containerdetail .el-col {
    padding: 0 10px; /* 列之间的间距 */
}

/* 行样式 */
.containerdetail .el-row {
    display: flex;
    flex-wrap: wrap;
    margin-left: -10px; /* 负间距抵消列的padding */
    margin-right: -10px; /* 负间距抵消列的padding */
}

.back-icon {
    display: flex;
    align-items: center;
    cursor: pointer;
    color: #007bff;
    font-size: 16px;
    margin-bottom: 20px;
}

.back-icon:hover {
    text-decoration: underline;
}

.back-icon i {
    margin-right: 5px;
}

img {
    width: 100%;
    height: auto;
    border-radius: 4px;
    margin-bottom: 20px;
}

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

.containerdetail a {
    color: #007bff;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

.containerdetail button {
    margin-top: 20px;
    padding: 10px 20px;
    font-size: 16px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.containerdetail button:hover {
    background-color: #0056b3;
}
</style>