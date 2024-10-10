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
    <div>
        淘宝账密设置
        <el-input v-model="form_tb.t_name" placeholder="请输入淘宝账号">
            <template #prefix>
                <el-icon>
                    <User />
                </el-icon>
            </template>
        </el-input>
        <el-input type="password" v-model="form_tb.t_password" placeholder="请输入淘宝账号密码" show-password>
            <template #prefix>
                <el-icon>
                    <Lock />
                </el-icon>
            </template>
        </el-input>
        <el-button type="primary" @click="submitTb">提交</el-button>
    </div>

    <div>
        <el-button type="primary" @click="startLoginJd">获取京东登录二维码</el-button>
        <el-button v-if="showRefresh" type="primary" @click="refreshQrcode">刷新二维码</el-button>
        <el-image src="" alt="description" fit="cover"></el-image>
        <img src="https://qr.m.jd.com/show?appid=133&size=147&t=1728487617936" alt="Smiley face" width="42" height="42">
    </div>
</template>

<script setup>
import { useStore } from 'vuex';
import { computed, ref, reactive } from 'vue';

import { notify } from '@/composables/utils'
import { modifyUser, addTb, addJd, getQrcode } from '@/api/api';

const store = useStore();
const editing = ref(false);
const showRefresh = ref(false);
const qrcodeUrl = ref('static/QrcodeFailed.png');

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

const form_tb = reactive({
    t_name: '',
    t_password: '',
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

const submitTb = () => {
    for (let key in form_tb) {
        if (!form_tb[key].trim()) { // 使用trim()去除可能的空白字符
            notify('error', "账号或密码不能为空")
            return;
        }
    }

    const User = store.state.user;
    const data = { ...form_tb }
    addTb(User.id, data)
        .then(res => {
            if (res.code === 200) {
                notify('success', res.message)
            } else {
                notify('error', res.message)
            }
        })
}

const startLoginJd = () => {
    showRefresh.value = true;
    const User = store.state.user;
    addJd(User.id) 
        .then(res => {
            if (res.code === 200) {
                showRefresh.value = false;
                notify('success', res.message)
            } else {
                notify('error', res.message)
            }
        })
}

const refreshQrcode = () => {
    getQrcode()
        .then(res => {
            if (res.code === 200) {
                qrcodeUrl.value = res.data
                notify('success', res.message)
            } else {
                notify('error', res.message)
            }
        })
}

</script>

<style scoped>
/* 你的样式 */
</style>