import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import axios from 'axios'  // 补充axios导入

axios.defaults.baseURL = 'http://localhost:8000'  // 提前到挂载前
const app = createApp(App)
app.use(ElementPlus)
app.mount('#app')
axios .defaults.baseURL = 'http://localhost:8000'