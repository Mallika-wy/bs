<template>
    <div class="body">
        <div class="container" id="login-box">
            <div>
                <h1 class="text-center" style="margin-bottom: 40px; margin-top: 40px;">注册</h1>
                <el-form ref="formRef" :rules="rules" :model="form">
                    <el-form-item prop="name" :label="用户名">
                        <el-input v-model="form.name" placeholder="请输入用户名">
                            <template #prefix>
                                <span>名称: </span>
                                <el-icon>
                                    <User />
                                </el-icon>
                            </template>
                        </el-input>
                    </el-form-item>
                    <el-form-item prop="password">
                        <el-input type="password" v-model="form.password" placeholder="请输入密码" show-password>
                            <template #prefix>
                                <span>密码: </span>
                                <el-icon>
                                    <Lock />
                                </el-icon>
                            </template>
                        </el-input>
                    </el-form-item>
                    <el-form-item prop="email">
                        <el-input v-model="form.email" placeholder="请输入邮箱">
                            <template #prefix>
                                <span>邮箱: </span>
                                <el-icon>
                                    <Lock />
                                </el-icon>
                            </template>
                        </el-input>
                    </el-form-item>
                    <el-form-item prop="phone">
                        <el-input v-model="form.phone" placeholder="请输入手机号">
                            <template #prefix>
                                <span>手机: </span>
                                <el-icon>
                                    <Phone />
                                </el-icon>
                            </template>
                        </el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-input v-model="form.address" placeholder="请输入地址">
                            <template #prefix>
                                <span>地址: </span>
                                <el-icon>
                                    <Phone />
                                </el-icon>
                            </template>
                        </el-input>
                    </el-form-item>
                    <el-form-item label="性别">
                        <el-radio-group v-model="form.sex">
                            <el-radio value="1">男性</el-radio>
                            <el-radio value="0">女性</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item>
                        <div class="button-container">
                            <el-button type="primary" @click="submitForm" :loading="loading">点击注册</el-button>
                            <el-button type="primary" @click="login" :loading="loading">返回登录</el-button>
                        </div>
                    </el-form-item>
                </el-form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

import { setToken } from '@/composables/cookie'
import { notify } from '@/composables/utils'
import { register } from '@/api/api'

const loading = ref(false)

const form = reactive({
    name: '',
    password: '',
    email: '',
    phone: '',
    sex: 1,
    address: ''
})

const store = useStore()

const router = useRouter()

const rules = {
    name: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
    ],
    password: [
        { required: true, trigger: "blur", message: "请输入您的密码" },
        {
            pattern: /^.{8,}$/,
            message: "用户密码长度必须大于8",
            trigger: "blur",
        },
        {
            pattern: /^(?![a-zA-Z]+$)(?![A-Z0-9]+$)(?![A-Z\W_!@#$%^&*`~()-+=]+$)(?![a-z0-9]+$)(?![a-z\W_!@#$%^&*`~()-+=]+$)(?![0-9\W_!@#$%^&*`~()-+=]+$)[a-zA-Z0-9\W_!@#$%^&*`~()-+=]/,
            message: "密码应包含数字、大写字母、小写字母、特殊符号中的3类",
            trigger: "blur",
        }
    ],
    email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
    ],
    phone: [
        { required: true, message: '请输入手机号', trigger: 'blur' },
        { pattern: /^1[3456789]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
    ]
}

const submitForm = () => {
    formRef.value.validate(valid => {
        if (!valid)
            return false
        loading.value = true
        const user_info_dict = {
            name: form.name,
            password: form.password,
            email: form.email,
            phone: form.phone,
            sex: form.sex,
            address: form.address
        }
        register(user_info_dict)
            .then(res => {
                console.log(res);
                if (res.code === 200) {
                    setToken(res.data.cookie)
                    store.commit('setUser', res.data)
                    console.log(res.data.id);
                    notify('success', res.message)
                    router.push('/User')
                } else {
                    notify('error', res.message)
                }
            }).finally(() => {
                loading.value = false
            });
    })
}

const login = () => {
    router.push('/login')
}

const formRef = ref(null)
</script>

<style scoped>
/* * {
    box-sizing: border-box;
} */

.body {
    font-family: 'Montserrat', sans-serif;
    /* 设置字体族， 如果系统没有Montserrat字体，就回退到sans-serif */
    background-image: linear-gradient(90deg, #dfb7d8 0%, #6B65EF 100%);
    /* 线性渐变背景: 120为角度 两种颜色 */
    display: flex;
    /* 弹性布局 */
    flex-direction: column;
    /* 垂直方向排列 */
    justify-content: center;
    /* 元素在主轴，水平居中对齐 */
    align-items: center;
    /* 元素在交叉轴上，垂直居中对齐 */
    height: 100vh;
    margin: 0 px;
}

h1 {
    font-weight: bold;
    margin: 0;
    font-size: 25px;
}

span {
    font-size: 20px;
}

.container {
    background: #ffffff;
    border-radius: 15px;
    box-shadow: 0 16px 32px rgba(0, 0, 0, .25), 0 10px 10px rgba(0, 0, 0, .22);
    position: relative;
    overflow: hidden;
    width: 800px;
    max-width: 100%;
    min-height: 540px;
    opacity: 1;
}

.el-form {
    width: 70%;
    max-width: 500px;
    margin: auto;
}

.el-form-item {
    margin-bottom: 40px;
    /* 增加表单项之间的间距 */
}

.el-input__inner,
.el-textarea__inner {
    border-radius: 5px;
    /* 输入框和文本区域的圆角 */
    border: 1px solid #dcdfe6;
    /* 边框颜色 */
    transition: border-color 0.3s;
    /* 边框颜色变化的过渡效果 */
}

.el-input__inner:focus,
.el-textarea__inner:focus {
    border-color: #409EFF;
    /* 输入框聚焦时的边框颜色 */
}

.el-button {
    border-radius: 20px;
    border: 1px solid #6B65EF;
    background: #6B65EF;
    color: #fff;
    font-size: 12px;
    font-weight: bold;
    padding: 12px 45px;
    letter-spacing: 1px;
    text-transform: uppercase;
    transition: transform 80ms ease-in;
    cursor: pointer;
}

.el-button:hover {
    background-color: #5962ae;
    /* 按钮悬浮时的背景颜色 */
}

.social-container {
    margin: 20px 0;
}

.button-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

/* .social-container a {
    border: 1px solid #ddd;
    border-radius: 50%;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    margin: 0 5px;
    height: 40px;
    width: 40px;
}

.social-container a:hover {
    background-color: #eee;

}

.txtb {
    border-bottom: 2px solid #adadad;
    position: relative;
    margin: 10px 0;
}

.txtb input {
    font-size: 15px;
    color: #333;
    border: none;
    width: 100%;
    outline: none;
    background: none;
    padding: 0 3px;
    height: 35px;
} */

/* .txtb span::before {
    content: attr(data-placeholder);
    position: absolute;
    top: 50%;
    left: 5px;
    color: #adadad;
    transform: translateY(-50%);
    transition: .5s;
}

.txtb span::after {
    content: '';
    position: absolute;
    left: 0%;
    top: 100%;
    width: 0%;
    height: 2px;
    background-image: linear-gradient(120deg, #a6c0fe 0%, #f68084 100%);
    transition: .5s;
}

.focus+span::before {
    top: -5px;
} */

/* .focus+span::after {
    width: 100%;
}

button {
    border-radius: 20px;
    border: 1px solid #ff4b2b;
    background: #ff4b2b;
    color: #fff;
    font-size: 12px;
    font-weight: bold;
    padding: 12px 45px;
    letter-spacing: 1px;
    text-transform: uppercase;
    transition: transform 80ms ease-in;
    cursor: pointer;
}

button:active {
    transform: scale(.95);
}

button:focus {
    outline: none;
} */

/* button.ghost {
    background: transparent;
    border-color: #fff;
}

.form-container {
    position: absolute;
    top: 0;
    height: 100%;
    transition: all .6s ease-in-out;
}

.form-container button {
    background-image: linear-gradient(120deg, #a6c0fe 0%, #f68084 100%);
    border: none;
    background-size: 200%;
    color: #fff;
    transition: .5s;
}

.form-container button:hover {
    background-position: right;
} */

/* .sign-in-container {
    left: 0;
    width: 50%;
    z-index: 2;
}

.sign-in-container form a {
    position: relative;
    left: 100px;
}

.sign-up-container {
    left: 0;
    width: 50%;
    z-index: 1;
    opacity: 0;
}

.sign-up-container button {
    margin-top: 20px;
} */

/* .overlay-container {
    position: absolute;
    top: 0;
    left: 50%;
    width: 50%;
    height: 100%;
    overflow: hidden;
    transition: transform .6s ease-in-out;
    z-index: 100;
} */

/* .overlay {
    background-image: linear-gradient(120deg, #a6c0fe 0%, #f68084 100%);
    color: #fff;
    position: relative;
    left: -100%;
    height: 100%;
    width: 200%;
    transform: translateY(0);
    transition: transform .6s ease-in-out;
} */

/* .overlay-panel {
    position: absolute;
    top: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 0 40px;
    height: 100%;
    width: 50%;
    text-align: center;
    transform: translateY(0);
    transition: transform .6s ease-in-out;
} */

/* .overlay-right {
    right: 0;
    transform: translateY(0);

} */

/* .overlay-left {
    transform: translateY(-20%);
} */

/* .container.right-panel-active .sign-in-container {
    transform: translateY(100%);
} */

/* .container.container.right-panel-active .overlay-container {
    transform: translateX(-100%);
} */

/* .container.right-panel-active .sign-up-container {
    transform: translateX(100%);
    opacity: 1;
    z-index: 5;
} */

/* .container.container.right-panel-active .overlay {
    transform: translateX(50%);
} */

/* .container.container.right-panel-active .overlay-left {
    transform: translateY(0);
} */

/* .container.container.right-panel-active .overlay-right {
    transform: translateY(20%);
} */

/* 设置选中后的文字颜色 */
/* .myCheckBox>>>.el-checkbox__input.is-checked+.el-checkbox__label {
    color: #333;
} */

/* 设置选中后对勾框的边框和背景颜色 */
/* .myCheckBox>>>.el-checkbox__input.is-checked .el-checkbox__inner,
.myCheckBox .el-checkbox__input.is-indeterminate .el-checkbox__inner {
    background-color: #f68084
} */

/* 设置checkbox获得焦点后，对勾框的边框颜色 */
/* .myCheckBox>>>.el-checkbox__input.is-focus .el-checkbox__inner {
    border-color: #f68084;
} */

/* 设置鼠标经过对勾框，对勾框边框的颜色 */
/* .myCheckBox>>>.el-checkbox__inner:hover {
    border-color: #f68084;
}  */
</style>