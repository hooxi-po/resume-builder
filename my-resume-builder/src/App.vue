<template>
  <div class="app-container">
    <header class="app-header">
      <div class="header-content" :class="{ 'full-width-header-content': isEditorRoute }">
        <router-link to="/" class="header-title-link"><h1>简历生成器</h1></router-link>
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

    <main class="main-content-routed" :class="{ 'full-width-content': isEditorRoute }">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <footer class="app-footer" v-if="!isEditorRoute">
      <p class="footer-note">© {{ new Date().getFullYear() }} 简历生成器. 保留所有权利.</p>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useAuthStore } from './stores/authStore'; // 确保路径正确
import { useRouter, useRoute } from 'vue-router';
// import { ElButton } from 'element-plus'; // 如果按需导入

const auth = useAuthStore();
const router = useRouter();
const route = useRoute();

const currentRouteName = computed(() => route.name);

const isEditorRoute = computed(() => {
  return route.name === 'resumeEdit' || route.name === 'resumeNew';
});

const handleLogout = () => {
  auth.logout();
  router.push({ name: 'login' });
};

const navigateToLogin = () => {
  router.push({ name: 'login' });
};

const navigateToRegister = () => {
  router.push({ name: 'register' });
};

auth.initAuth();
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: #f4f7f9;
  color: #333;
}

.app-header {
  background-color: #ffffff;
  color: #2c3e50;
  /* padding 内边距由 .header-content 控制 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  border-bottom: 1px solid #e0e0e0;
  width: 100%;
  box-sizing: border-box;
  flex-shrink: 0;
  position: sticky; /* 使页眉在所有页面都固定 */
  top: 0;
  z-index: 1000; /* 确保在其他内容之上 */
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  /* 默认情况下，头部内容区是居中且有最大宽度的 */
  max-width: 1200px;
  margin: 0 auto;
  padding: 0.8rem 2rem; /* 默认内边距 */
  transition: max-width 0.3s ease, padding 0.3s ease, margin 0.3s ease;
}

/* 当是编辑器路由时，头部内容区也全宽 */
.header-content.full-width-header-content {
  max-width: none;
  /* 确保编辑器页面的全局页眉内边距与 ResumeEditorView 自己的页眉内边距协调 */
  /* ResumeEditorView 的 .editor-header padding 是 10px 25px */
  padding: 0.8rem 25px; /* 例如，保持垂直方向一致，水平方向与编辑器头部一致 */
  margin: 0;
}

.header-title-link {
  text-decoration: none;
  color: inherit;
}

.app-header h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.main-navigation {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.main-navigation a {
  text-decoration: none;
  color: #333;
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
  transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out;
}

.main-navigation a:hover,
.main-navigation a.router-link-exact-active {
  background-color: #e9ecef;
}

.user-greeting {
  font-size: 0.9rem;
  color: #555;
  margin-right: 0.5rem;
}

.main-content-routed {
  flex-grow: 1;
  width: 100%;
  box-sizing: border-box;
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem;
  transition: max-width 0.3s ease, padding 0.3s ease, margin 0.3s ease;
  display: flex;
  flex-direction: column;
}

.main-content-routed.full-width-content {
  max-width: none;
  padding: 0; /* 编辑器视图自己控制其内部边距 */
  margin: 0;
}

.app-footer {
  background-color: #ffffff;
  padding: 1.5rem 2rem;
  text-align: center;
  border-top: 1px solid #e0e0e0;
  color: #777;
  font-size: 0.85rem;
  width: 100%;
  box-sizing: border-box;
  flex-shrink: 0;
}

.footer-note {
  margin: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
