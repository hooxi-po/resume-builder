<template>
  <div class="resume-editor-view">
    <el-container v-if="auth.isAuthenticated" class="editor-container-flex">
      <el-header class="editor-header">
        <div class="header-left">
          <el-input
            v-if="currentResumeData"
            v-model="currentResumeData.resume_name"
            placeholder="请输入简历名称"
            class="resume-title-input"
            size="large"
            @blur="handleResumeNameBlur"
          />
          <span v-else class="header-placeholder">加载中...</span>
        </div>
        <div class="header-right">
          <el-button @click="goBack" icon="ArrowLeft" round>返回列表</el-button>
          <el-button type="primary" @click="saveResume" :loading="resumeStore.isLoading" icon="Check" round>
            {{ resumeStore.isLoading ? '保存中...' : '保存简历' }}
          </el-button>
          <el-button type="success" @click="generateAndDownloadPdf" :loading="isGeneratingPdf" icon="Download" round>
            {{ isGeneratingPdf ? '生成PDF中...' : '下载PDF' }}
          </el-button>
          </div>
      </el-header>

      <el-main v-if="currentResumeData" class="editor-main-content">
        <div class="editor-layout">
          <section class="editor-pane">
            <h2 class="pane-title visually-hidden">编辑简历内容</h2>
            <div class="form-sections-container">
              <PersonalInfoForm :resume-data="currentResumeData.resume_data" />
              <EducationForm :resume-data="currentResumeData.resume_data" />
              <ExperienceForm :resume-data="currentResumeData.resume_data" />
              <SkillsForm :resume-data="currentResumeData.resume_data" />
              </div>
          </section>

          <section class="preview-pane" ref="resumePreviewPaneRef">
            <h2 class="pane-title visually-hidden">简历预览</h2>
            <div class="preview-wrapper" id="resumePreviewContent">
              <BasicTemplate :resumeData="currentResumeData.resume_data" />
            </div>
          </section>
        </div>
      </el-main>
      <el-main v-else-if="resumeStore.isLoading" class="loading-placeholder">
         <el-skeleton :rows="10" animated />
      </el-main>
      <el-main v-else-if="resumeStore.error" class="error-placeholder">
         <el-alert :title="resumeStore.error || '加载简历数据失败'" type="error" show-icon center :closable="false" />
         <el-button @click="goBack" style="margin-top: 20px;">返回列表</el-button>
      </el-main>
    </el-container>
    <div v-else class="auth-required-placeholder">
      <p>请先 <router-link :to="{ name: 'login' }">登录</router-link> 以编辑简历。</p>
    </div>

    <div class="fixed-action-bar" v-if="auth.isAuthenticated">
        <el-tooltip effect="dark" content="设置" placement="left">
            <el-button icon="Setting" circle />
        </el-tooltip>
        <el-tooltip effect="dark" content="帮助" placement="left">
            <el-button icon="QuestionFilled" circle />
        </el-tooltip>
        <el-tooltip effect="dark" content="反馈" placement="left">
            <el-button icon="ChatDotSquare" circle />
        </el-tooltip>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
// 使用相对路径导入 store
import { useAuthStore } from '../stores/authStore.js';
import { useResumeStore } from '../stores/resumeStore.js';
// 引入 Element Plus 组件
import { ElMessage, ElInput, ElButton, ElHeader, ElMain, ElContainer, ElSkeleton, ElAlert, ElTooltip } from 'element-plus';
import html2pdf from 'html2pdf.js';

// 使用相对路径导入组件
import PersonalInfoForm from '../components/forms/PersonalInfoForm.vue';
import EducationForm from '../components/forms/EducationForm.vue';
import ExperienceForm from '../components/forms/ExperienceForm.vue';
import SkillsForm from '../components/forms/SkillsForm.vue';
import BasicTemplate from '../components/templates/BasicTemplate.vue';

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();
const resumeStore = useResumeStore();

const currentResumeData = computed(() => resumeStore.currentResume);
const isGeneratingPdf = ref(false);
const resumePreviewPaneRef = ref(null);

onMounted(async () => {
  if (!auth.isAuthenticated) {
    router.push({ name: 'login', query: { redirect: route.fullPath } });
    return;
  }

  const resumeId = route.params.id;
  if (resumeId) {
    await resumeStore.fetchResumeById(resumeId);
    if (resumeStore.error) {
        ElMessage.error(resumeStore.error || '加载简历失败');
    }
  } else {
    resumeStore.createNewLocalResume();
  }
});

const handleResumeNameBlur = () => {
  // Logic for when resume name input loses focus
};

const saveResume = async () => {
  if (!currentResumeData.value) {
    ElMessage.error('没有可保存的简历数据');
    return;
  }
  const savedResume = await resumeStore.saveCurrentResume();
  if (resumeStore.error) {
    ElMessage.error(resumeStore.error || '保存失败');
  } else {
    ElMessage.success('简历已保存！');
    if (!route.params.id && savedResume?._id) {
      router.replace({ name: 'resumeEdit', params: { id: savedResume._id } });
    }
  }
};

const generateAndDownloadPdf = async () => {
  if (!currentResumeData.value || !currentResumeData.value.resume_data) {
    ElMessage.error('没有简历内容可以生成PDF。');
    return;
  }
  isGeneratingPdf.value = true;
  ElMessage.info('正在生成PDF，请稍候...');

  const element = document.getElementById('resumePreviewContent');
  if (!element) {
    ElMessage.error('无法找到简历预览区域。');
    isGeneratingPdf.value = false;
    return;
  }

  const resumeName = currentResumeData.value.resume_name || '未命名简历';
  const filename = `${resumeName.replace(/\s+/g, '_')}_${new Date().toISOString().slice(0,10)}.pdf`;

  const opt = {
    margin:       [5, 5, 5, 5],
    filename:     filename,
    image:        { type: 'jpeg', quality: 0.98 },
    html2canvas:  { scale: 2, useCORS: true, logging: false, scrollY: 0 },
    jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' },
    pagebreak:    { mode: ['avoid-all', 'css', 'legacy'] }
  };

  try {
    const pdfExporter = html2pdf().from(element).set(opt);
    await pdfExporter.save();
    ElMessage.success('PDF已成功生成并开始下载！');
  } catch (error) {
    console.error("PDF生成失败:", error);
    ElMessage.error('PDF生成失败，请查看控制台获取更多信息。');
  } finally {
    isGeneratingPdf.value = false;
  }
};

const goBack = () => {
  router.push({ name: 'home' });
};

watch(() => route.params.id, async (newId, oldId) => {
  if (!auth.isAuthenticated) {
    return;
  }
  if (newId && newId !== oldId && route.name === 'resumeEdit') {
    await resumeStore.fetchResumeById(newId);
      if (resumeStore.error) {
        ElMessage.error(resumeStore.error || '加载简历失败');
    }
  } else if (!newId && route.name === 'resumeNew' && oldId !== undefined) {
    resumeStore.createNewLocalResume();
  }
}, { immediate: false });

</script>

<style scoped>
.resume-editor-view {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background-color: #f0f2f5;
}

.editor-container-flex {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 25px;
  background-color: #ffffff;
  border-bottom: 1px solid #e0e0e0;
  height: 60px;
  flex-shrink: 0;
}

.header-left {
  flex-grow: 1;
  margin-right: 20px;
}
.resume-title-input {
  font-size: 1.2rem;
  font-weight: bold;
}
.resume-title-input :deep(.el-input__wrapper) {
  box-shadow: none !important;
  border-radius: 0;
}
.resume-title-input :deep(.el-input__inner) {
  border: none !important;
  padding-left: 0;
}
.header-placeholder {
  font-size: 1.2rem;
  font-weight: bold;
  color: #c0c4cc;
}

.header-right {
  display: flex;
  gap: 12px;
}

.editor-main-content {
  padding: 0;
  overflow: hidden;
  flex-grow: 1;
  display: flex;
}

.editor-layout {
  display: flex;
  flex-grow: 1;
  width: 100%;
  height: calc(100vh - 60px); /* 减去头部高度 */
}

.editor-pane {
  /* 修改: 增加编辑框宽度 */
  flex: 0 0 500px; /* 左侧固定宽度设为500px */
  background-color: #2c3e50; 
  color: #ecf0f1; 
  padding: 20px;
  overflow-y: auto; 
  box-sizing: border-box;
  transition: width 0.3s ease;
}
.editor-pane::-webkit-scrollbar {
  width: 8px;
}
.editor-pane::-webkit-scrollbar-track {
  background: #2c3e50; 
}
.editor-pane::-webkit-scrollbar-thumb {
  background: #4e6a85; 
  border-radius: 4px;
}
.editor-pane::-webkit-scrollbar-thumb:hover {
  background: #5a7b9a;
}

.preview-pane {
  /* 修改: 确保预览框占据剩余空间 */
  flex: 1; /* flex-grow: 1, flex-shrink: 1, flex-basis: 0% */
  background-color: #f0f2f5; 
  padding: 20px;
  overflow-y: auto;
  box-sizing: border-box;
  display: flex;
  justify-content: center;
}
.preview-wrapper {
  width: 100%;
  max-width: 820px; 
}

.pane-title.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  margin: -1px;
  padding: 0;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}

.form-sections-container {
  /* Styles for form sections container */
}

.loading-placeholder, .error-placeholder, .auth-required-placeholder {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
  padding: 20px;
  text-align: center;
}

.fixed-action-bar {
    position: fixed;
    top: 50%;
    right: 0px;
    transform: translateY(-50%);
    display: flex;
    flex-direction: column;
    gap: 10px;
    background-color: rgba(255, 255, 255, 0.9);
    padding: 10px 8px;
    border-radius: 8px 0 0 8px;
    box-shadow: -2px 0 8px rgba(0,0,0,0.1);
    z-index: 1000;
}
.fixed-action-bar .el-button {
    margin: 0 !important;
}
</style>
