import axios from 'axios'
import { notify } from '@/composables/utils'
// import { useCookies } from '@vueuse/integrations/useCookies';

const service = axios.create({
  baseURL: 'http://127.0.0.1:5000'
})

// 添加请求拦截器
service.interceptors.request.use(function (config) {
  // 有空再实现
  // const cookie = useCookies()
  // const token = cookie.get('token')
  // console.log(token)
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
  // 对响应数据做点什么
  return response.data;
}, function (error) {
  // 对响应错误做点什么
  notify('error', '请求失败')
  
  return Promise.reject(error);
});

export default service