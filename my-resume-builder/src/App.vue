<template>
  <div class="app-container">
    <header class="app-header">
      <div class="header-content">
        <h1>简历生成器</h1>
        <nav class="main-navigation">
          <router-link to="/" v-if="auth.isAuthenticated">我的简历</router-link>
          <span v-if="auth.isAuthenticated" class="user-greeting">
            欢迎, {{ auth.currentUser?.username || auth.currentUser?.email }}!
          </span>
          <el-button type="primary" @click="navigateToLogin" v-if="!auth.isAuthenticated && currentRouteName !== 'login'">
            登录
          </el-button>
          <el-button @click="navigateToRegister" v-if="!auth.isAuthenticated && currentRouteName !== 'register'">
            注册
          </el-button>
          <el-button type="danger" @click="handleLogout" v-if="auth.isAuthenticated">
            登出
          </el-button>
        </nav>
      </div>
    </header>

    <main class="main-content-routed">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <footer class="app-footer">
      <p class="footer-note">© {{ new Date().getFullYear() }} 简历生成器. 保留所有权利.</p>
      </footer>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useAuthStore } from './stores/authStore'; // 假设您的Pinia认证store
import { useRouter, useRoute } from 'vue-router';   // 导入Vue Router的hooks

const auth = useAuthStore();
const router = useRouter();
const route = useRoute(); // 获取当前路由信息

// 计算当前路由的名称，用于动态显示登录/注册按钮
const currentRouteName = computed(() => route.name);

const handleLogout = () => {
  auth.logout();
  router.push({ name: 'login' }); // 登出后导航到登录页
};

const navigateToLogin = () => {
  router.push({ name: 'login' });
};

const navigateToRegister = () => {
  router.push({ name: 'register' });
};

onMounted(() => {
  // 应用加载时尝试从localStorage或sessionStorage恢复认证状态
  // 这个逻辑现在应该在 authStore.initAuth() 中处理
  auth.initAuth();
});
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: #f4f7f9; /* 淡雅的背景色 */
  color: #333;
}

.app-header {
  background-color: #ffffff; /* 白色头部 */
  color: #2c3e50; /* 深色文字 */
  padding: 0.8rem 2rem; /* 调整内边距 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); /* 轻微阴影 */
  border-bottom: 1px solid #e0e0e0;
  position: sticky; /* 使头部固定 */
  top: 0;
  z-index: 1000; /* 确保在其他内容之上 */
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px; /* 限制内容最大宽度 */
  margin: 0 auto; /* 居中 */
}

.app-header h1 {
  margin: 0;
  font-size: 1.5rem; /* 调整标题大小 */
  font-weight: 600;
  cursor: pointer; /* 可选：如果标题是首页链接 */
}
.app-header h1:hover {
  /* color: var(--el-color-primary); 可选：Element Plus 主题色 */
}

.main-navigation {
  display: flex;
  align-items: center;
  gap: 1rem; /* 导航项之间的间距 */
}

.main-navigation a {
  text-decoration: none;
  color: #333;
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
  transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out;
}

.main-navigation a:hover,
.main-navigation a.router-link-exact-active { /* 当前激活路由的样式 */
  background-color: #e9ecef;
  /* color: var(--el-color-primary); */
}

.user-greeting {
  font-size: 0.9rem;
  color: #555;
  margin-right: 0.5rem;
}

.main-content-routed {
  flex-grow: 1;
  padding: 1.5rem; /* 主内容区内边距 */
  width: 100%;
  max-width: 1200px; /* 限制内容最大宽度 */
  margin: 0 auto; /* 居中 */
  box-sizing: border-box;
}

.app-footer {
  background-color: #ffffff;
  padding: 1.5rem 2rem;
  text-align: center;
  border-top: 1px solid #e0e0e0;
  color: #777;
  font-size: 0.85rem;
}

.footer-note {
  margin: 0;
}

/* 路由切换过渡效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Element Plus 按钮的微调 (如果需要) */
.main-navigation .el-button {
  /* margin-left: 0.5rem; */
}
</style>
