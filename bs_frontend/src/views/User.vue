<template>
    <div v-if="!editing" class="card-container">
        <el-card>
            <p style="padding: 2.5px;"><span style="font-weight: bold;">Username: </span>{{ $store.state.user.name }}
            </p>
            <p style="padding: 2.5px;"><span style="font-weight: bold;">Telephone: </span>{{ $store.state.user.phone }}
            </p>
            <p style="padding: 2.5px;"><span style="font-weight: bold;">性别: </span>{{ sexText }}</p>
            <p style="padding: 2.5px;"><span style="font-weight: bold;">email: </span>{{ $store.state.user.email }}</p>
            <p style="padding: 2.5px;"><span style="font-weight: bold;">Address: </span>{{ $store.state.user.address }}
            </p>
            <el-button type="primary" @click="startEdit">编辑</el-button>
        </el-card>
    </div>
    <div v-else class="card-container">
        <el-card>
            <el-form :model="form" label-width="auto" style="max-width: 600px">
                <el-form-item label="用户名">
                    <el-input v-model="form.name" />
                </el-form-item>
                <el-form-item label="电话号码">
                    <el-input v-model="form.phone" />
                </el-form-item>
                <el-form-item label="邮箱">
                    <el-input v-model="form.email" />
                </el-form-item>
                <el-form-item label="地址">
                    <el-input v-model="form.address" />
                </el-form-item>
                <el-form-item label="性别">
                    <el-radio-group v-model="form.sex">
                        <el-radio value="1">男性</el-radio>
                        <el-radio value="0">女性</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item>
                    <el-button @click="submitEdit">提交</el-button>
                    <el-button @click="cancelEdit">返回</el-button>
                </el-form-item>
            </el-form>
        </el-card>
    </div>
</template>

<script setup>
import { useStore } from 'vuex';
import { computed, ref, reactive } from 'vue';

import { notify } from '@/composables/utils'
import { modifyUser } from '@/api/api';

const store = useStore();
const editing = ref(false);

const sexText = computed(() => {
    const sex = store.state.user.sex;
    return sex === 1 ? '男性' : (sex === 0 ? '女性' : '未知');
});

const form = reactive({
    name: '',
    phone: '',
    email: '',
    address: '',
    sex: null
})


const startEdit = () => {
    editing.value = true;
    form.name = store.state.user.name;
    form.phone = store.state.user.phone;
    form.sex = store.state.user.sex;
    form.email = store.state.user.email;
    form.address = store.state.user.address;
};

const cancelEdit = () => {
    editing.value = false;
    form.name = '';
    form.phone = '';
    form.sex = null;
    form.email = '';
    form.address = '';
};

const submitEdit = () => {
    const originalUser = store.state.user;
    const modifiedUser = { ...form }

    const hasChanges = Object.keys(modifiedUser).some(key => modifiedUser[key] !== originalUser[key]);

    if (hasChanges) {
        modifyUser(originalUser.id, modifiedUser)
            .then(res => {
                if (res.code === 200) {
                    notify('success', res.message)
                    store.commit('setUser', res.data)
                } else {
                    notify('error', res.message)
                }
            });
    } else {
        notify('error', "没有任何修改")
    }
};
</script>

<style scoped>
.image-container {
    padding: 30px;
    /* 根据需要调整大小 */
    background-color: white;
    /* 设置背景颜色为白色 */
}

.card-container {
    max-width: 90%;
    /* 卡片容器的最大宽度 */
    margin: 15px auto;
    /* 上下边距为20px，左右自动（自动边距使容器居中） */
    padding: 15px;
    /* 内边距 */
    text-align: center;
    /* 文本居中 */
}

/* 卡片样式 */
.card-container .el-card {
    display: inline-block;
    /* 使卡片能够水平居中 */
    width: 100%;
    /* 卡片宽度为容器的100% */
    margin: 0;
    /* 移除卡片的默认外边距 */
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    /* 轻微的阴影效果 */
}

/* 卡片内部段落样式 */
.card-container p {
    margin: 5px 0;
    /* 段落之间的间距 */
}

.card-container .el-button {
  background-color: #409EFF;
  color: white;
  border-color: #409EFF;
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 4px;
  display: block;
  width: auto;
  margin: 10px auto;
}

.card-container .el-button:hover {
    background-color: #66b1ff;
    /* 按钮悬停时背景颜色 */
    border-color: #66b1ff;
    /* 按钮悬停时边框颜色 */
}
</style>