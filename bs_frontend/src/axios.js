import axios from 'axios'
import { notify } from '@/composables/utils'
// import { useCookies } from '@vueuse/integrations/useCookies';

const service = axios.create({
  baseURL: 'http://127.0.0.1:5000'
  // baseURL: 'http://172.29.101.55:5000'
})

// 添加请求拦截器
service.interceptors.request.use(function (config) {
  // 有空再实现
  // const cookie = useCookies()
  // const token = cookie.get('token')
  // if (token) {
  //   config.headers[token] = token
  // }
  return config;
}, function (error) {
  // 对请求错误做些什么
  return Promise.reject(error);
});

// 添加响应拦截器
service.interceptors.response.use(function (response) {
  return response.data;
}, function (error) {
  // 对响应错误做点什么
  notify('error', error.response.data.message)
  return Promise.reject(error);
});

export default service