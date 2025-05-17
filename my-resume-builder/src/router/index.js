// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue'; // 假设的主页视图 (例如简历列表)
import LoginView from '../views/LoginView.vue'; // 假设的登录视图
import RegisterView from '../views/RegisterView.vue'; // 假设的注册视图
import ResumeEditorView from '../views/ResumeEditorView.vue'; // 假设的简历编辑视图
import NotFoundView from '../views/NotFoundView.vue'; // 假设的404页面 (可选)

// 导入 Pinia store - 确保路径正确
// 假设您的 stores 文件夹在 src/stores
import { useAuthStore } from '../stores/authStore';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView, // 或者您的简历列表/仪表盘页面
    meta: { requiresAuth: true } // 标记此路由需要认证
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { guestOnly: true } // 标记此路由只对未登录用户开放
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: { guestOnly: true }
  },
  {
    path: '/resume/edit/:id', // 编辑现有简历
    name: 'resumeEdit',
    component: ResumeEditorView,
    props: true, // 将路由参数 :id 作为 props 传递给组件
    meta: { requiresAuth: true }
  },
  {
    path: '/resume/new', // 创建新简历
    name: 'resumeNew',
    component: ResumeEditorView,
    // props: route => ({ id: null }), // 可以这样传递一个null的id，或者在组件内部处理
    meta: { requiresAuth: true }
  },
  // 可选: 添加一个通配符路由来捕获所有未匹配的路径 (404页面)
  {
    path: '/:pathMatch(.*)*', // Vue Router 4.x 的通配符语法
    name: 'NotFound',
    component: NotFoundView
  }
  // 您可以添加更多路由，例如用户账户设置等
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // 使用 HTML5 History 模式
  routes,
  scrollBehavior(to, from, savedPosition) {
    // 路由切换时，滚动到页面顶部或保持之前的位置
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  }
});

// 全局前置导航守卫
router.beforeEach((to, from, next) => {
  // 在导航守卫内部获取 store 实例，确保 Pinia 已初始化
  // 注意：如果 Pinia 尚未完全初始化（例如在 main.js 中 app.use(pinia) 之前），这里可能会出问题
  // 通常在 main.js 中 app.use(router) 之前 app.use(pinia) 可以避免此问题
  const authStore = useAuthStore();

  const isAuthenticated = authStore.isAuthenticated; // 从 store 获取认证状态
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const guestOnly = to.matched.some(record => record.meta.guestOnly);

  if (requiresAuth && !isAuthenticated) {
    // 如果路由需要认证但用户未认证，重定向到登录页
    // 可以传递一个查询参数 redirect，以便登录后返回原页面
    console.log('Navigation Guard: Requires auth, not authenticated. Redirecting to login.');
    next({ name: 'login', query: { redirect: to.fullPath } });
  } else if (guestOnly && isAuthenticated) {
    // 如果路由只对未登录用户开放但用户已认证，重定向到主页
    console.log('Navigation Guard: Guest only, authenticated. Redirecting to home.');
    next({ name: 'home' });
  } else {
    // 其他情况，正常导航
    console.log(`Navigation Guard: Proceeding to ${to.name || to.path}`);
    next();
  }
});

export default router;
