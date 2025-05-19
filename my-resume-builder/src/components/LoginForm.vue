<template>
  <div class="login-form-container">
    <el-card class="login-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <h2>用户登录</h2>
        </div>
      </template>
      <el-form
        ref="loginFormRef"
        :model="loginData"
        :rules="loginRules"
        label-position="top"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="邮箱 (用作用户名)" prop="email">
          <el-input
            v-model="loginData.email"
            placeholder="请输入您的邮箱地址"
            clearable
            size="large"
            prefix-icon="Message"
          />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginData.password"
            type="password"
            placeholder="请输入您的密码"
            show-password
            clearable
            size="large"
            prefix-icon="Lock"
          />
        </el-form-item>
        <el-form-item v-if="auth.loginError">
          <el-alert
            :title="auth.loginError"
            type="error"
            show-icon
            :closable="false"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            native-type="submit"
            class="login-button"
            :loading="auth.isLoading"
            size="large"
            round
          >
            {{ auth.isLoading ? '登录中...' : '登 录' }}
          </el-button>
        </el-form-item>
      </el-form>
      <div class="form-footer">
        <p>
          还没有账户?
          <router-link :to="{ name: 'register' }">立即注册</router-link>
        </p>
        </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onUnmounted } from 'vue';
import { useAuthStore } from '/home/leven/24-25/resume-builder/my-resume-builder/src/stores/authStore.js'; // 确保 路径 正确
import { useRouter, useRoute } from 'vue-router';
// 按需导入 Element Plus 图标 (如果未全局注册)
// import { Message, Lock } from '@element-plus/icons-vue'; // 在模板中直接使用字符串名称也可

const loginFormRef = ref(null); // 用于访问 el-form 实例
const auth = useAuthStore();
const router = useRouter();
const route = useRoute(); // 获取当前路由信息，用于登录后重定向

const loginData = reactive({
  email: '',
  password: '',
});

// 表单验证规则
const loginRules = reactive({
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: ['blur', 'change'] },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' },
  ],
});

const handleLogin = async () => {
  if (!loginFormRef.value) return;
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      const success = await auth.login({
        email: loginData.email,
        password: loginData.password,
      });
      if (success) {
        // 登录成功后，检查路由查询参数中是否有 redirect
        const redirectPath = route.query.redirect || '/'; // 默认为首页
        router.push(redirectPath);
        console.log('登录成功，用户信息:', auth.currentUser);
      }
    } else {
      console.log('表单验证失败!');
      return false;
    }
  });
};

// 组件卸载时清除登录错误信息，避免下次进入页面时还显示
onUnmounted(() => {
  if (auth.loginError) {
    auth.loginError = null;
  }
});
</script>

<style scoped>
.login-form-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 150px); /* 减去大致的页眉页脚高度 */
  padding: 20px;
  background-color: #f4f7f9; /* 与 App.vue 背景色一致或类似 */
}

.login-card {
  width: 100%;
  max-width: 420px;
  border-radius: 8px;
}

.card-header {
  text-align: center;
}
.card-header h2 {
  margin: 0;
  font-size: 1.8rem;
  color: #303133; /* Element Plus 主要文字颜色 */
}

.login-button {
  width: 100%;
}

.form-footer {
  text-align: center;
  margin-top: 20px;
  font-size: 0.9rem;
}

.form-footer p {
  margin: 8px 0;
}

.form-footer a {
  color: var(--el-color-primary); /* Element Plus 主题色 */
  text-decoration: none;
}

.form-footer a:hover {
  text-decoration: underline;
}

/* Element Plus 表单项的标签样式调整 */
:deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266; /* Element Plus 次要文字颜色 */
}
</style>
