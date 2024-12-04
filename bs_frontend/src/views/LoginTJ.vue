<template>
    <!-- <div class="TB">
        <div class="text">淘宝登录</div>
        <div>
            <el-input v-model="form_account.t_name" placeholder="请输入淘宝账号">
                <template #prefix>
                    <el-icon>
                        <User />
                    </el-icon>
                </template>
            </el-input>
            <p></p>
            <el-input type="password" v-model="form_account.t_password" placeholder="请输入淘宝账号密码" show-password>
                <template #prefix>
                    <el-icon>
                        <Lock />
                    </el-icon>
                </template>
            </el-input>
            <p></p>
            <el-button round color="#626aef" class="w-[100px]" type="primary" @click="loginTb">提交</el-button>
        </div>
    </div> -->

    <div class="TB">
        <div class="text">淘宝登录</div>
        <div>
            <div>
                <el-button round color="#626aef" class="w-[200px]" type="primary"
                    @click="startLoginTb">获取淘宝登录二维码</el-button>
                <el-button v-if="showRefreshTb" round color="#626aef" class="w-[100px]" type="primary"
                    @click="refreshQrcodeTb">刷新二维码</el-button>
            </div>
            <div class="image-container" v-if="showImageTb">
                <el-image :src="'data:image/*;base64,' + qrcodeTb" alt="description" fit="cover"
                    v-if="showQrcodeTb"></el-image>
                <el-image src="public/static/QrcodeFailed.png" alt="description" fit="cover"
                    v-if="!showQrcodeTb"></el-image>
            </div>
        </div>
    </div>


    <hr class="hr-twill">

    <div class="JD">
        <div class="text">京东登录</div>
        <div>
            <div>
                <el-button round color="#626aef" class="w-[200px]" type="primary"
                    @click="startLoginJd">获取京东登录二维码</el-button>
                <el-button v-if="showRefreshJd" round color="#626aef" class="w-[100px]" type="primary"
                    @click="refreshQrcodeJd">刷新二维码</el-button>
            </div>
            <div class="image-container" v-if="showImageJd">
                <el-image :src="'data:image/*;base64,' + qrcodeJd" alt="description" fit="cover"
                    v-if="showQrcodeJd"></el-image>
                <el-image src="public/static/QrcodeFailed.png" alt="description" fit="cover"
                    v-if="!showQrcodeJd"></el-image>
            </div>
        </div>
    </div>


</template>


<script setup>
import { useStore } from 'vuex';
import { ref, reactive } from 'vue';

import { notify } from '@/composables/utils'
import { addTb, addJd, getQrcode } from '@/api/api';

const store = useStore();

const showRefreshTb = ref(false);
const showImageTb = ref(false);
const showQrcodeTb = ref(false);

const showRefreshJd = ref(false);
const showImageJd = ref(false);
const showQrcodeJd = ref(false);



// const form_account = reactive({
//     t_name: '',
//     t_password: '',
// })

const qrcodeTb = ref('');
const qrcodeJd = ref('');

// const loginTb = () => {
//     for (let key in form_account) {
//         if (!form_account[key].trim()) { // 使用trim()去除可能的空白字符
//             notify('error', "账号或密码不能为空")
//             return;
//         }
//     }

//     const User = store.state.user;
//     const data = { ...form_account }
//     addTb(User.id, data)
//         .then(res => {
//             if (res.code === 200) {
//                 notify('success', res.message)
//             } else {
//                 notify('error', res.message)
//             }
//         })
// }

const startLoginTb = () => {
    showRefreshTb.value = true;
    showImageTb.value = true;
    const User = store.state.user;
    notify('info', '请稍等..., 大约等待3秒')
    addTb(User.id)
        .then(res => {
            if (res.code === 200) {
                notify('success', res.message)
            } else {
                notify('error', res.message)
            }
            showRefreshTb.value = false;
            showImageTb.value = false
        })
}

const refreshQrcodeTb = () => {
    getQrcode()
        .then(res => {
            if (res.code === 200) {
                showQrcodeTb.value = true
                qrcodeTb.value = res.data
                notify('success', res.message)
            } else {
                notify('error', res.message)
            }
        })
}

const startLoginJd = () => {
    showRefreshJd.value = true;
    showImageJd.value = true;
    const User = store.state.user;
    notify('info', '请稍等..., 大约等待3秒')
    addJd(User.id)
        .then(res => {
            if (res.code === 200) {
                notify('success', res.message)
            } else {
                notify('error', res.message)
            }
            showRefreshJd.value = false;
            showImageJd.value = false
        })
}

const refreshQrcodeJd = () => {
    getQrcode()
        .then(res => {
            if (res.code === 200) {
                showQrcodeJd.value = true
                qrcodeJd.value = res.data
                notify('success', res.message)
            } else {
                notify('error', res.message)
            }
        })
}
</script>


<style scoped>
.TB {
    height: 50%;
}

.JD {
    height: 50%;
}

.text {
    font-weight: bold;
    /* 加粗 */
    font-size: 18px;
    /* 字号 */
    margin-left: 6px;
    /* 与左边留空间的大小 */
    margin-bottom: 20px;
    color: #333;
    /* 文字颜色 */
    line-height: 1.6;
    /* 行高 */
    letter-spacing: 0.5px;
    /* 字间距 */
}

.el-input {
    width: 50%;
    /* 宽度占比 */
    max-width: 400px;
    /* 最大宽度 */
    height: 45px;
    /* 高度 */
    margin-bottom: 20px;
    /* 适当的间距 */
    border: 1px solid #dcdfe6;
    /* 边框颜色 */
    border-radius: 4px;
    /* 边框圆角 */
    transition: border-color 0.3s;
    /* 边框颜色变化的过渡效果 */
}

.el-input__inner:focus {
    border-color: #409EFF;
    /* 聚焦时边框颜色 */
    outline: none;
    /* 去除聚焦时的轮廓线 */
}

.el-input__inner {
    font-size: 18px;
    /* 字号 */
    color: #606266;
    /* 字体颜色 */
}

.el-input:hover {
    box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
    /* 鼠标悬浮时的阴影效果 */
}

.el-input {
    transition: all 0.3s ease-in-out;
}

.el-input:focus-within {
    transform: translateY(-2px);
    /* 聚焦时轻微上移，增加立体感 */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    /* 聚焦时的阴影效果 */
}

.hr-twill {
    border: 0;
    padding: 3px;
    background: repeating-linear-gradient(135deg, #a2a9b6 0px, #a2a9b6 1px, transparent 1px, transparent 6px);
}

.image-container {
    position: relative;
    display: inline-block;
    /* 或者使用 block，取决于你希望图片如何显示 */
    margin: 20px;
    /* 为图片容器添加一些外边距 */
    text-align: center;
    /* 使图片居中显示 */
}

.el-image {
    width: 200px;
    /* 设置图片的宽度 */
    height: 200px;
    /* 设置图片的高度 */
    border-radius: 10px;
    /* 为图片添加圆角 */
    border: 2px solid #409EFF;
    /* 为图片添加边框，颜色为 Element UI 的主题色 */
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    /* 添加阴影，使图片更具立体感 */
    transition: transform 0.3s ease;
    /* 添加变换的过渡效果 */
}

.el-image:hover {
    transform: scale(1.05);
    /* 鼠标悬停时放大图片 */
}
</style>