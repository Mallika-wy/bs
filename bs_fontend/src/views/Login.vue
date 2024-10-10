<template>

  <el-row style="min-height: 100vh;" class="bg-indigo-500">
    <el-col :lg="16" :md="12" class="flex items-center justify-center flex-col">
      <div class="font-bold text-5xl text-light-50 mb-8">商品比价网站</div>
      <div class="text-1xl text-gray-200 mt-8">浙江大学2024-2025秋冬学期B/S体系软件设计 课程项目</div>
    </el-col>
    <el-col :lg="8" :md="12" class="bg-light-50 flex items-center justify-center flex-col">
      <h2 class="font-bold text-3xl text-gray-800 mb-6">用户登录</h2>
      <el-form ref="formRef" :rules="rules" :model="form">
        <el-form-item prop="name">
          <el-input v-model="form.name" placeholder="请输入用户名">
            <template #prefix>
              <el-icon>
                <User />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input type="password" v-model="form.password" placeholder="请输入密码" show-password>
            <template #prefix>
              <el-icon>
                <Lock />
              </el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item class="mt-8">
          <el-button type="primary" @click="onSubmit" :loading="loading">登录</el-button>
          <el-button>注册</el-button>
        </el-form-item>
      </el-form>
    </el-col>
  </el-row>
</template>


<script setup>
import { ref, reactive } from 'vue'
import { login } from '@/api/api'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

import { setToken } from '@/composables/cookie'
import { notify } from '@/composables/utils'

const loading = ref(false)

const form = reactive({
  name: '',
  password: ''
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
  ]
}

const formRef = ref(null)

const onSubmit = () => {
  formRef.value.validate(valid => {
    if (!valid)
      return false
    loading.value = true
    login(form.name, form.password)
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
</script>

<style></style>