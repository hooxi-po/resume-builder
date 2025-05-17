import { defineStore } from 'pinia';
import apiClient from '../services/api'; // 导入我们创建的apiClient
// 如果您使用了Vue Router，可以导入它以便在action中导航
// import router from '../router'; 

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('accessToken') || null,
    user: JSON.parse(localStorage.getItem('user')) || null, // 当前用户信息
    loginError: null,
    registerError: null,
    isLoading: false,
  }),
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
    currentUser: (state) => state.user,
  },
  actions: {
    setToken(token) {
      this.accessToken = token;
      localStorage.setItem('accessToken', token);
    },
    setUser(userData) {
      this.user = userData;
      localStorage.setItem('user', JSON.stringify(userData));
    },
    clearAuthData() {
      this.accessToken = null;
      this.user = null;
      localStorage.removeItem('accessToken');
      localStorage.removeItem('user');
    },
    async login(credentials) { // credentials 应该是一个对象 { username: 'email', password: 'password' }
      this.isLoading = true;
      this.loginError = null;
      try {
        // 注意：FastAPI的OAuth2PasswordRequestForm期望的是表单数据，
        // 而axios默认发送JSON。我们需要调整Content-Type或数据格式。
        // 后端auth_router.py中 OAuth2PasswordRequestForm = Depends() 会处理表单数据
        const formData = new URLSearchParams();
        formData.append('username', credentials.email); // FastAPI中form_data.username对应邮箱
        formData.append('password', credentials.password);

        const response = await apiClient.post('/auth/login/access-token', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        });

        const { access_token } = response.data;
        this.setToken(access_token);

        // 登录成功后获取用户信息
        await this.fetchCurrentUser();

        // 导航到主页或仪表盘 (如果使用了Vue Router)
        // router.push('/'); 
        return true;
      } catch (error) {
        this.loginError = error.response?.data?.detail || '登录失败，请检查您的凭据。';
        console.error('登录错误:', error);
        this.clearAuthData();
        return false;
      } finally {
        this.isLoading = false;
      }
    },
    async register(userData) { // userData: { email, username, password }
      this.isLoading = true;
      this.registerError = null;
      try {
        const response = await apiClient.post('/auth/register', userData);
        // 注册成功后，可以选择自动登录或提示用户去登录
        // 这里我们不自动登录，而是返回用户信息，提示用户去登录页
        console.log('注册成功:', response.data);
        return response.data; // 返回创建的用户信息
      } catch (error) {
        this.registerError = error.response?.data?.detail || '注册失败，请重试。';
        console.error('注册错误:', error);
        return null;
      } finally {
        this.isLoading = false;
      }
    },
    async fetchCurrentUser() {
      if (!this.accessToken) return; // 如果没有token，则不获取
      this.isLoading = true;
      try {
        const response = await apiClient.get('/auth/me');
        this.setUser(response.data);
      } catch (error) {
        console.error('获取当前用户信息失败:', error);
        // Token可能失效，清除认证数据并可能重定向到登录
        if (error.response && error.response.status === 401) {
            this.logout(); // 或者直接调用 clearAuthData
            // router.push('/login');
        }
      } finally {
        this.isLoading = false;
      }
    },
    logout() {
      this.clearAuthData();
      // 导航到登录页 (如果使用了Vue Router)
      // router.push('/login'); 
      console.log('用户已登出');
    },
    // 应用启动时尝试加载用户
    async initAuth() {
        if (this.accessToken && !this.user) {
            await this.fetchCurrentUser();
        }
    }
  },
});