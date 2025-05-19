// src/services/api.js
import axios from 'axios';

// 创建一个axios实例
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api', // 从环境变量读取API基础URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// 添加请求拦截器，用于在每个请求的头部附加JWT Token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken'); // 或者从Pinia/Vuex store获取
    
    // --- DEBUGGING START ---
    console.log('[Request Interceptor] 发起请求到:', config.url);
    console.log('[Request Interceptor] 当前 localStorage 中的 Token:', token);
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
      console.log('[Request Interceptor] Authorization 请求头已设置:', config.headers['Authorization']);
    } else {
      console.log('[Request Interceptor] localStorage 中未找到 Token.');
    }
    console.log('[Request Interceptor] 发出请求的完整配置头:', config.headers);
    // --- DEBUGGING END ---

    return config;
  },
  (error) => {
    console.error('[Request Interceptor] 请求配置错误:', error);
    return Promise.reject(error);
  }
);

// （可选）添加响应拦截器，用于统一处理错误或Token刷新等
apiClient.interceptors.response.use(
  (response) => {
    console.log('[Response Interceptor] 收到响应来自:', response.config.url, '状态码:', response.status);
    return response;
  },
  (error) => {
    console.error('[Response Interceptor] API 错误状态码:', error.response?.status);
    console.error('[Response Interceptor] API 错误数据:', error.response?.data);
    console.error('[Response Interceptor] API 错误配置:', error.config);


    if (error.response && error.response.status === 401) {
      console.error('未授权或Token已过期 (来自响应拦截器):', error.response.data);
      // 例如：Token失效，可以尝试刷新Token或重定向到登录页
      // localStorage.removeItem('accessToken'); // 清除失效的Token
      // localStorage.removeItem('user');
      // 这里的跳转逻辑最好由 authStore 或路由守卫处理，以避免循环依赖或在非组件上下文操作路由
      // if (window.location.pathname !== '/login') {
      //   // router.push('/login'); // 如果 router 实例在这里可用
      // }
    }
    return Promise.reject(error);
  }
);

export default apiClient;
