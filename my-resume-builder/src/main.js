// src/main.js

import { createApp } from 'vue'; // 导入 Vue 的 createApp 函数
import { createPinia } from 'pinia'; // 导入 Pinia 的 createPinia 函数

import App from './App.vue'; // 导入根组件 App.vue
import router from './router'; // 导入路由配置 (假设您在 src/router/index.js 或 src/router.js 中配置了路由)

import ElementPlus from 'element-plus'; // 导入 Element Plus
import 'element-plus/dist/index.css'; // 引入 Element Plus 样式

// 可选: 导入其他全局 CSS 文件
// import './assets/main.css'; // 例如，一个包含全局样式的文件

// 创建 Vue 应用实例
const app = createApp(App);

// 创建 Pinia 实例
const pinia = createPinia();

// 使用 Element Plus 插件
app.use(ElementPlus);

// 使用 Pinia 插件
// 这使得 Pinia store 可以在整个应用中被访问
app.use(pinia);

// 使用 Vue Router 插件
// 这使得 <router-link> 和 <router-view> 组件可用，并启用路由功能
app.use(router);

// 将 Vue 应用实例挂载到 HTML 页面中具有 id="app" 的元素上
// 这个 #app 通常在 public/index.html 文件中定义
app.mount('#app');

// 可选: 如果您需要在应用启动时执行一些初始化逻辑 (例如从 Pinia store 加载初始数据)
// 可以在这里或在 App.vue 的 onMounted 钩子中进行
// import { useAuthStore } from './stores/authStore'; // 假设您的 authStore
// const authStore = useAuthStore(pinia); // 在 use Pinia 之后，但在 mount 之前初始化 store (如果需要在 setup 之外访问)
// authStore.initAuth(); // 例如，尝试从 localStorage 恢复用户登录状态
