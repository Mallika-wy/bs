import { createApp } from 'vue'
import App from './App.vue'
import '@/style.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from './router'
import store from './store'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
import githubTheme from '@kangc/v-md-editor/lib/theme/github';
import '@kangc/v-md-editor/lib/theme/style/github.css';

VMdPreview.use(githubTheme);

const app = createApp(App)

app.use(store)
app.use(router)
app.use(ElementPlus)
app.use(VMdPreview);
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

import 'virtual:windi.css'

import './permission'

import "nprogress/nprogress.css"

app.mount('#app')
