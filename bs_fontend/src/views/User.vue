<template>
    <div v-if="!editing">
        <el-descriptions title="用户信息" direction="vertical" :column="2">
            <el-descriptions-item label="Username">{{ $store.state.user.name }}</el-descriptions-item>
            <el-descriptions-item label="Telephone">{{ $store.state.user.phone }}</el-descriptions-item>
            <el-descriptions-item label="性别">{{ sexText }}</el-descriptions-item>
            <el-descriptions-item label="email">{{ $store.state.user.email }}</el-descriptions-item>
            <el-descriptions-item label="Address" :span="2">{{ $store.state.user.address }}</el-descriptions-item>
        </el-descriptions>
        <el-button type="primary" @click="startEdit">编辑</el-button>
    </div>
    <div v-else>

        <el-button type="primary" @click="submitEdit">提交</el-button>
        <el-button @click="cancelEdit">返回</el-button>

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
                <el-button type="primary" @click="submitEdit">Create</el-button>
                <el-button>Cancel</el-button>
            </el-form-item>
        </el-form>
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
  padding: 30px; /* 根据需要调整大小 */
  background-color: white; /* 设置背景颜色为白色 */
}
</style>