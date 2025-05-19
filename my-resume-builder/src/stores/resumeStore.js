// src/stores/resumeStore.js
import { defineStore } from 'pinia';
import apiClient from '../services/api';
import { useAuthStore } from './authStore';

const defaultNewResumeData = () => ({
  personalInfo: { name: '', avatar: '', title: '', email: '', phone: '', linkedin: '', github: '', website: '', address: '', city: '', country: '' },
  summary: '',
  experience: [],
  education: [],
  projects: [],
  skills: { technical: [], languages: [], soft: [] },
  certificates: [],
  customSections: [],
  meta: { template: 'BasicTemplate', accentColor: '#007bff', fontFamily: 'Arial, sans-serif' },
});

export const useResumeStore = defineStore('resume', {
  state: () => ({
    currentResume: null,
    userResumes: [],
    isLoading: false,
    error: null,
  }),
  getters: {
    currentResumeContent: (state) => state.currentResume?.resume_data || null,
  },
  actions: {
    async fetchUserResumes() {
      const authStore = useAuthStore();
      if (!authStore.isAuthenticated) {
        this.error = '用户未认证，无法获取简历列表。';
        console.warn('fetchUserResumes called without authentication.');
        return;
      }
      this.isLoading = true;
      this.error = null;
      try {
        const response = await apiClient.get('/resumes');
        console.log('Fetched user resumes raw response.data:', JSON.parse(JSON.stringify(response.data)));
        this.userResumes = response.data; // 期望 response.data 中的对象使用 _id
        console.log('resumeStore.userResumes after assignment:', JSON.parse(JSON.stringify(this.userResumes)));
      } catch (err) {
        this.error = err.response?.data?.detail || '获取简历列表失败。';
        console.error('Error fetching user resumes:', err.response || err);
      } finally {
        this.isLoading = false;
      }
    },

    async fetchResumeById(resumeId) { // resumeId 期望是 _id
      const authStore = useAuthStore();
      if (!authStore.isAuthenticated) {
        this.error = '用户未认证，无法获取简历。';
        return;
      }
      this.isLoading = true;
      this.error = null;
      this.currentResume = null;
      try {
        const response = await apiClient.get(`/resumes/${resumeId}`); // 后端期望路径中的 resumeId 是 _id
        console.log(`Fetched resume by ID (${resumeId}) raw response.data:`, JSON.parse(JSON.stringify(response.data)));
        this.currentResume = response.data; // 期望 response.data 中的对象使用 _id
        console.log(`resumeStore.currentResume after assignment (ID: ${resumeId}):`, JSON.parse(JSON.stringify(this.currentResume)));
      } catch (err) {
        this.error = err.response?.data?.detail || `获取简历 (ID: ${resumeId}) 失败。`;
        console.error(`Error fetching resume ${resumeId}:`, err.response || err);
      } finally {
        this.isLoading = false;
      }
    },
    
    createNewLocalResume() {
      const newResumeDataContent = JSON.parse(JSON.stringify(defaultNewResumeData()));
      this.currentResume = {
        // _id: undefined, // 新建的本地简历在保存到后端前没有 _id
        resume_name: '未命名简历',
        resume_data: newResumeDataContent,
      };
      this.error = null;
      console.log('Created new local resume structure:', JSON.parse(JSON.stringify(this.currentResume)));
    },

    async saveCurrentResume() {
      const authStore = useAuthStore();
      if (!authStore.isAuthenticated) {
        this.error = '用户未认证，无法保存简历。';
        return null;
      }
      if (!this.currentResume || !this.currentResume.resume_data) {
        this.error = '没有当前简历数据可保存。';
        console.error('saveCurrentResume called with no current resume data.');
        return null;
      }
      if (!this.currentResume.resume_name || this.currentResume.resume_name.trim() === '') {
        this.error = '简历名称不能为空。';
        console.error('Resume name cannot be empty.');
        return null;
      }
      this.isLoading = true;
      this.error = null;
      const resumeDataPayload = JSON.parse(JSON.stringify(this.currentResume.resume_data));
      
      // 清理 resumeDataPayload 中的空字符串为 null (如果后端期望如此)
      const pi = resumeDataPayload.personalInfo;
      if (pi) {
        if (pi.avatar === '') pi.avatar = null;
        if (pi.linkedin === '') pi.linkedin = null;
        if (pi.github === '') pi.github = null;
        if (pi.website === '') pi.website = null;
      }

      if (resumeDataPayload.projects && Array.isArray(resumeDataPayload.projects)) {
        resumeDataPayload.projects.forEach(proj => {
          if (proj.url === '') proj.url = null;
          if (proj.repoUrl === '') proj.repoUrl = null;
        });
      }

      if (resumeDataPayload.certificates && Array.isArray(resumeDataPayload.certificates)) {
        resumeDataPayload.certificates.forEach(cert => {
          if (cert.credentialUrl === '') cert.credentialUrl = null;
        });
      }
      
      const payload = {
        resume_name: this.currentResume.resume_name.trim(),
        resume_data: resumeDataPayload,
      };
      
      console.log("Payload to be sent to backend:", JSON.parse(JSON.stringify(payload)));
      if (this.currentResume._id) { // 前端现在使用 _id
        console.log("Saving existing resume with _ID:", this.currentResume._id);
      } else {
        console.log("Creating new resume (no _ID yet).");
      }

      try {
        let response;
        if (this.currentResume._id) { // 使用 this.currentResume._id
          response = await apiClient.put(`/resumes/${this.currentResume._id}`, payload);
        } else {
          response = await apiClient.post('/resumes', payload);
        }
        console.log('Save/Create resume raw response.data:', JSON.parse(JSON.stringify(response.data)));
        this.currentResume = response.data; // 后端应返回包含 _id 的完整简历对象
        console.log('resumeStore.currentResume after save/create:', JSON.parse(JSON.stringify(this.currentResume)));
        
        await this.fetchUserResumes();
        return response.data;
      } catch (err) {
        let errorMessages = "保存简历失败：";
        if (err.response && err.response.data && err.response.data.detail) {
            const errorDetails = err.response.data.detail;
            if (Array.isArray(errorDetails)) {
                errorMessages += errorDetails.map(e => {
                    const loc = e.loc && Array.isArray(e.loc) ? e.loc.join('.') : '解析错误位置失败';
                    const msg = e.msg || '未知验证错误';
                    return `${loc} - ${msg}`;
                }).join('; ');
            } else if (typeof errorDetails === 'string') {
                errorMessages += errorDetails;
            } else {
                errorMessages += JSON.stringify(errorDetails); 
            }
        } else if (err.message) {
            errorMessages += err.message;
        } else {
            errorMessages += '发生未知错误。';
        }
        this.error = errorMessages;
        console.error('Error saving resume:', err.response || err);
        return null;
      } finally {
        this.isLoading = false;
      }
    },

    async deleteResume(resumeId) { // resumeId 期望是 _id
      const authStore = useAuthStore();
      if (!authStore.isAuthenticated) {
        this.error = '用户未认证，无法删除简历。';
        return false;
      }
      this.isLoading = true;
      this.error = null;
      try {
        await apiClient.delete(`/resumes/${resumeId}`); // 后端期望路径中的 resumeId 是 _id
        // 使用 _id 进行过滤
        this.userResumes = this.userResumes.filter(r => r._id !== resumeId);
        // 检查 currentResume._id
        if (this.currentResume && this.currentResume._id === resumeId) {
          this.currentResume = null;
        }
        return true;
      } catch (err) {
        this.error = err.response?.data?.detail || `删除简历 (ID: ${resumeId}) 失败。`;
        console.error(`Error deleting resume ${resumeId}:`, err.response || err);
        return false;
      } finally {
        this.isLoading = false;
      }
    },

    updateCurrentResumeName(name) {
        if (this.currentResume) {
            this.currentResume.resume_name = name;
        }
    },

    updateCurrentResumeDataContent(resumeDataContent) {
        if (this.currentResume) {
            this.currentResume.resume_data = resumeDataContent;
        }
    },

    clearCurrentResume() {
        this.currentResume = null;
        this.error = null;
    }
  },
});
