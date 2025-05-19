<template>
  <div class="register-form-container">
    <el-card class="register-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <h2>用户注册</h2>
        </div>
      </template>
      <el-form
        ref="registerFormRef"
        :model="registerData"
        :rules="registerRules"
        label-position="top"
        @submit.prevent="handleRegister"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="registerData.username"
            placeholder="请输入您的用户名"
            clearable
            size="large"
            prefix-icon="User"
          />
        </el-form-item>
        <el-form-item label="邮箱地址" prop="email">
          <el-input
            v-model="registerData.email"
            placeholder="请输入您的邮箱地址"
            clearable
            size="large"
            prefix-icon="Message"
          />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerData.password"
            type="password"
            placeholder="请输入您的密码 (至少6位)"
            show-password
            clearable
            size="large"
            prefix-icon="Lock"
          />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="registerData.confirmPassword"
            type="password"
            placeholder="请再次输入您的密码"
            show-password
            clearable
            size="large"
            prefix-icon="Lock"
          />
        </el-form-item>
        <el-form-item v-if="auth.registerError">
          <el-alert
            :title="auth.registerError"
            type="error"
            show-icon
            :closable="false"
          />
        </el-form-item>
        <el-form-item v-if="registerSuccessMessage">
          <el-alert
            :title="registerSuccessMessage"
            type="success"
            show-icon
            :closable="false"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            native-type="submit"
            class="register-button"
            :loading="auth.isLoading"
            size="large"
            round
          >
            {{ auth.isLoading ? '注册中...' : '注 册' }}
          </el-button>
        </el-form-item>
      </el-form>
      <div class="form-footer">
        <p>
          已有账户?
          <router-link :to="{ name: 'login' }">立即登录</router-link>
        </p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onUnmounted } from 'vue';
import { useAuthStore } from '/home/leven/24-25/resume-builder/my-resume-builder/src/stores/authStore.js'; // 确保路径正确
import { useRouter } from 'vue-router';
// 按需导入 Element Plus 图标 (如果未全局注册)
// import { User, Message, Lock } from '@element-plus/icons-vue';

const registerFormRef = ref(null);
const auth = useAuthStore();
const router = useRouter();

const registerData = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
});

const registerSuccessMessage = ref('');

// 自定义确认密码验证规则
const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'));
  } else if (value !== registerData.password) {
    callback(new Error('两次输入的密码不一致!'));
  } else {
    callback();
  }
};

const registerRules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度应在3到50个字符之间', trigger: 'blur' },
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: ['blur', 'change'] },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' },
  ],
});

const handleRegister = async () => {
  if (!registerFormRef.value) return;
  registerSuccessMessage.value = ''; // 清除之前的成功消息
  auth.registerError = null; // 清除之前的错误消息

  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      const userData = {
        username: registerData.username,
        email: registerData.email,
        password: registerData.password,
      };
      const createdUser = await auth.register(userData);
      if (createdUser) {
        registerSuccessMessage.value = `注册成功！用户 ${createdUser.username} 已创建。现在您可以登录了。`;
        // 可选：几秒后自动跳转到登录页
        setTimeout(() => {
          router.push({ name: 'login' });
        }, 3000); // 3秒后跳转
      }
      // auth.registerError 会在 store action 中被设置
    } else {
      console.log('表单验证失败!');
      return false;
    }
  });
};

// 组件卸载时清除注册错误和成功消息
onUnmounted(() => {
  if (auth.registerError) {
    auth.registerError = null;
  }
  registerSuccessMessage.value = '';
});
</script>

<style scoped>
.register-form-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 150px); /* 减去大致的页眉页脚高度 */
  padding: 20px;
  background-color: #f4f7f9;
}

.register-card {
  width: 100%;
  max-width: 480px; /* 比登录卡片稍宽，因为字段更多 */
  border-radius: 8px;
}

.card-header {
  text-align: center;
}
.card-header h2 {
  margin: 0;
  font-size: 1.8rem;
  color: #303133;
}

.register-button {
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
  color: var(--el-color-primary);
  text-decoration: none;
}

.form-footer a:hover {
  text-decoration: underline;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
}
</style>
