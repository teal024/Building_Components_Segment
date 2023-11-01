import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'// 导入路由配置文件
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import store from './store';

const app = createApp(App)
app.use(ElementPlus)
app.use(router)
app.use(store)
app.mount('#app')

