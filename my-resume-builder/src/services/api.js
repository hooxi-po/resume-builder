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
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// （可选）添加响应拦截器，用于统一处理错误或Token刷新等
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      // 例如：Token失效，可以尝试刷新Token或重定向到登录页
      console.error('Unauthorized or Token expired:', error.response.data);
      // localStorage.removeItem('accessToken'); // 清除失效的Token
      // window.location.href = '/login'; // 或者使用Vue Router导航
    }
    return Promise.reject(error);
  }
);

export default apiClient;