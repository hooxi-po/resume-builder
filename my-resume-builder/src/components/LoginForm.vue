<template>
  <div class="login-form">
    <h2>用户登录</h2>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="email">邮箱 (用作用户名):</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div>
        <label for="password">密码:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit" :disabled="auth.isLoading">
        {{ auth.isLoading ? '登录中...' : '登录' }}
      </button>
      <p v-if="auth.loginError" class="error-message">{{ auth.loginError }}</p>
    </form>
    <p>还没有账户? <router-link to="/register">立即注册</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/authStore';
import { useRouter } from 'vue-router'; // 如果使用Vue Router

const email = ref('');
const password = ref('');
const auth = useAuthStore();
const router = useRouter(); // 如果使用Vue Router

const handleLogin = async () => {
  const success = await auth.login({ email: email.value, password: password.value });
  if (success) {
    // 登录成功后的导航，例如到用户仪表盘或简历编辑页
    router.push('/'); // 假设根路径是受保护的或主页
    console.log('登录成功，用户信息:', auth.currentUser);
  }
};
</script>

<style scoped>
.login-form { max-width: 400px; margin: auto; padding: 20px; border: 1px solid #ccc; border-radius: 5px; }
.login-form div { margin-bottom: 15px; }
.login-form label { display: block; margin-bottom: 5px; }
.login-form input { width: 100%; padding: 8px; box-sizing: border-box; }
.error-message { color: red; margin-top: 10px; }
</style>