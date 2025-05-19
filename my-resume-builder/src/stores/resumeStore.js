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
        this.userResumes = response.data;
      } catch (err) {
        this.error = err.response?.data?.detail || '获取简历列表失败。';
        console.error('Error fetching user resumes:', err.response || err);
      } finally {
        this.isLoading = false;
      }
    },

    async fetchResumeById(resumeId) {
      const authStore = useAuthStore();
      if (!authStore.isAuthenticated) {
        this.error = '用户未认证，无法获取简历。';
        return;
      }
      this.isLoading = true;
      this.error = null;
      this.currentResume = null;
      try {
        const response = await apiClient.get(`/resumes/${resumeId}`);
        this.currentResume = response.data;
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
        resume_name: '未命名简历',
        resume_data: newResumeDataContent,
      };
      this.error = null;
      console.log('Created new local resume structure:', this.currentResume);
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

      // MODIFICATION: Frontend validation for resume_name
      if (!this.currentResume.resume_name || this.currentResume.resume_name.trim() === '') {
        this.error = '简历名称不能为空。';
        // 如果您在store中也想使用Element Plus的ElMessage，需要确保它已正确配置或传递
        // import { ElMessage } from 'element-plus'; // 通常不在store中直接使用UI组件的通知
        console.error('Resume name cannot be empty.');
        return null;
      }

      this.isLoading = true;
      this.error = null;

      const resumeDataPayload = JSON.parse(JSON.stringify(this.currentResume.resume_data));

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
        resume_name: this.currentResume.resume_name.trim(), // MODIFICATION: Trim the resume name
        resume_data: resumeDataPayload,
      };
      
      // console.log("Payload to be sent:", JSON.stringify(payload, null, 2)); // Uncomment for debugging

      try {
        let response;
        if (this.currentResume.id) {
          response = await apiClient.put(`/resumes/${this.currentResume.id}`, payload);
        } else {
          response = await apiClient.post('/resumes', payload);
        }
        this.currentResume = response.data;
        await this.fetchUserResumes();
        return response.data;
      } catch (err) {
        // MODIFICATION: More robust error message parsing
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

    async deleteResume(resumeId) {
      const authStore = useAuthStore();
      if (!authStore.isAuthenticated) {
        this.error = '用户未认证，无法删除简历。';
        return false;
      }
      this.isLoading = true;
      this.error = null;
      try {
        await apiClient.delete(`/resumes/${resumeId}`);
        this.userResumes = this.userResumes.filter(r => r.id !== resumeId);
        if (this.currentResume && this.currentResume.id === resumeId) {
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
