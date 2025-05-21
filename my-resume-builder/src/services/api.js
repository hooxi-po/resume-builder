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
    
    console.log('[Request Interceptor] 发起请求到:', config.url);
    // console.log('[Request Interceptor] 当前 localStorage 中的 Token:', token); // 出于安全考虑，可以注释掉生产环境的token打印
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
      // console.log('[Request Interceptor] Authorization 请求头已设置.'); // 简化日志
    } else {
      console.log('[Request Interceptor] localStorage 中未找到 Token.');
    }
    // console.log('[Request Interceptor] 发出请求的完整配置头:', config.headers); // 包含Token，按需打印
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
    // --- 可选的调试日志 ---
    // console.log('[Response Interceptor] response.data:', JSON.parse(JSON.stringify(response.data)));
    return response;
  },
  (error) => {
    console.error('[Response Interceptor] API 错误状态码:', error.response?.status);
    console.error('[Response Interceptor] API 错误数据:', error.response?.data);
    // console.error('[Response Interceptor] API 错误配置:', error.config); // 包含请求的详细信息，按需打印

    if (error.response && error.response.status === 401) {
      console.error('未授权或Token已过期 (来自响应拦截器):', error.response.data?.detail || 'No details');
      // 例如：Token失效，可以尝试刷新Token或重定向到登录页
      // 实际项目中，这里通常会调用 authStore 的 action 来处理登出或 token 刷新
      // import { useAuthStore } from '@/stores/authStore'; // 避免循环依赖，通常在 main.js 或插件中处理
      // const authStore = useAuthStore();
      // authStore.logout(); // 示例
      // window.location.href = '/login'; // 强制跳转
    }
    return Promise.reject(error); // 确保错误继续传递，以便组件或 store 中的 catch 块可以处理
  }
);

// New function for AI content suggestions
export const getAIContentSuggestions = async (suggestionRequest) => {
  try {
    const response = await apiClient.post('/ai/suggest-content', suggestionRequest);
    return response.data; // Return the JSON response from the API
  } catch (error) {
    // The error interceptor should handle logging and generic error messages.
    // Specific handling can be done in the component calling this function.
    console.error('Error in getAIContentSuggestions:', error.response?.data || error.message);
    throw error; // Re-throw to allow component-level error handling
  }
};

export default apiClient;
