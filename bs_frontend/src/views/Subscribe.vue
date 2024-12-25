<template>
    <div class="subscribecontainer" v-if="!itemVisible">
        <el-button type="primary" @click="checkSubscribesEvent">一键检查</el-button>
        <el-row :gutter="20">
            <el-col :xs="24" :sm="12" :md="8" :lg="8" v-for="item in form.subscribe_list" :key="item.subscribe_id">
                <el-card>
                    <div style="margin-left: 10px; text-align: start; font-size: 16px;">
                        <p style="padding: 2.5px;"><span style="font-weight: bold;">订阅ID: </span>{{ item.subscribe_id }}
                        </p>
                        <p style="padding: 2.5px;"><span style="font-weight: bold;">商品名称: </span>{{ item.title }}</p>
                        <p style="padding: 2.5px;"><span style="font-weight: bold;">商品价格: </span>{{ item.price }}</p>
                    </div>
                    <el-button type="primary" @click="viewItem(item)">查看</el-button>
                    <el-button type="primary" @click="checkSubscribeEvent(item)">检查</el-button>
                    <el-button type="primary" @click="deleteSubscribeEvent(item)">删除</el-button>
                </el-card>
            </el-col>
        </el-row>
    </div>

    <div v-if="itemVisible">
        <div @click="closeDetail" class="back-icon">
            <el-icon>
                <ArrowLeft />
            </el-icon>
            返回订阅管理界面
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
                <p><strong>商品原链接：</strong><a :href="form.detail.item_url" target="_blank">{{ form.detail.item_url }}</a>
                </p>
            </el-col>
        </el-row>
        <p><strong>历史价格查询：</strong><img :src="'data:image/png;base64,' + form.detail.history_image" alt="历史价格查询" /></p>
        <el-button @click="subscribe">降价通知</el-button>
    </div>
</template>

<script setup>
import { useStore } from 'vuex'
import { reactive, ref } from 'vue';
import { onMounted } from 'vue'

import { notify } from '@/composables/utils'
import { getSubscribe, deleteSubscribe, checkSubscribe, checkSubscribes, searchItem } from '@/api/api';

const store = useStore()
const User = store.state.user;

const form = reactive({
    subscribe_list: [],
    detail: {}
})
const itemVisible = ref(false)

onMounted(() => {
    getSubscribe(User.id)
        .then(res => {
            form.subscribe_list = res.data
            notify('success', res.message)
        })
})

const deleteSubscribeEvent = (row) => {
    deleteSubscribe(User.id, row.subscribe_id)
        .then(res => {
            if (res.code === 200) {
                notify('success', res.message)
                const index = form.subscribe_list.findIndex(sub => sub.subscribe_id === row.subscribe_id);
                // 如果找到了，就从subscribe_list中删除这条记录
                if (index !== -1) {
                    form.subscribe_list.splice(index, 1);
                }
            } else {
                notify('error', res.message)
            }
        })
};

const checkSubscribeEvent = (row) => {
    checkSubscribe(User.id, row.subscribe_id)
        .then(res => {
            if (res.code === 200) {
                notify('success', res.message)
            } else {
                notify('error', res.message)
            }
        })
};

const checkSubscribesEvent = () => {
    checkSubscribes(User.id)
        .then(res => {
            if (res.code === 200) {
                notify('success', res.message)
            } else {
                notify('error', res.message)
            }
        })
};

const viewItem = (row) => {
    searchItem(User.id, row.item_id)
        .then(res => {
            if (res.code === 200) {
                notify('success', res.message)
                form.detail = res.data
                itemVisible.value = true
            } else {
                notify('error', res.message)
            }
        })
};

const closeDetail = () => {
    itemVisible.value = false
    form.detail = {}

}
</script>

<style scope>
.subscribecontainer {
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    max-width: 1200px;
    margin: 0 auto;
}

.el-button {
    margin-top: 10px;
    margin-right: 0px;
    background-color: #409EFF;
    color: white;
    border-color: #409EFF;
}

.el-button:hover {
    background-color: #66b1ff;
    border-color: #66b1ff;
}

.el-card {
    margin-bottom: 20px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.back-icon {
    cursor: pointer;
    color: #409EFF;
    font-size: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    background-color: #ECF5FF;
    border-radius: 4px;
    border: 1px solid #DCDFE6;
    margin-bottom: 20px;
}

.back-icon:hover {
    color: #66b1ff;
    border-color: #66b1ff;
}

.containerdetail {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.containerdetail .el-col {
    padding: 0 10px;
}

.containerdetail img {
    width: 100%;
    height: auto;
    margin-bottom: 20px;
}
</style>