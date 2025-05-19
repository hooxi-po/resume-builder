<template>
  <div class="resume-editor-view">
    <el-container v-if="auth.isAuthenticated">
      <el-header class="editor-header">
        <div class="header-left">
          <el-input
            v-if="currentResumeData"
            v-model="currentResumeData.resume_name"
            placeholder="请输入简历名称"
            class="resume-title-input"
            size="large"
          />
          <span v-else>加载中...</span>
        </div>
        <div class="header-right">
          <el-button @click="goBack" icon="ArrowLeft" round>返回列表</el-button>
          <el-button type="success" @click="saveResume" :loading="resumeStore.isLoading" icon="Check" round>
            {{ resumeStore.isLoading ? '保存中...' : '保存简历' }}
          </el-button>
          <el-button type="info" @click="previewResume" icon="View" round>预览PDF (待实现)</el-button>
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

          <section class="preview-pane">
            <h2 class="pane-title visually-hidden">简历预览</h2>
            <div class="preview-wrapper">
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
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '/home/leven/24-25/resume-builder/my-resume-builder/src/stores/authStore.js';
import { useResumeStore } from '/home/leven/24-25/resume-builder/my-resume-builder/src/stores/resumeStore.js'; // 您需要创建这个 store
import { ElMessage } from 'element-plus';

// 导入您之前创建的表单和模板组件
// 路径可能需要根据您的项目结构调整
import PersonalInfoForm from '/home/leven/24-25/resume-builder/my-resume-builder/src/components/forms/PersonalInfoForm.vue';
import EducationForm from '/home/leven/24-25/resume-builder/my-resume-builder/src/components/forms/EducationForm.vue';
import ExperienceForm from '/home/leven/24-25/resume-builder/my-resume-builder/src/components/forms/ExperienceForm.vue';
import SkillsForm from '/home/leven/24-25/resume-builder/my-resume-builder/src/components/forms/SkillsForm.vue';
import BasicTemplate from '/home/leven/24-25/resume-builder/my-resume-builder/src/components/templates/BasicTemplate.vue';

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();
const resumeStore = useResumeStore();

// 直接引用 store 中的 currentResume，它应该是响应式的
const currentResumeData = computed(() => resumeStore.currentResume);

onMounted(async () => {
  if (!auth.isAuthenticated) {
    router.push({ name: 'login', query: { redirect: route.fullPath } });
    return;
  }

  const resumeId = route.params.id;
  if (resumeId) {
    // 编辑现有简历
    await resumeStore.fetchResumeById(resumeId);
    if (resumeStore.error) {
        ElMessage.error(resumeStore.error || '加载简历失败');
    }
  } else {
    // 创建新简历
    resumeStore.createNewLocalResume(); // 这个 action 应该在 store 中初始化一个空的、符合前端结构的简历对象
  }
});

const saveResume = async () => {
  if (!currentResumeData.value) {
    ElMessage.error('没有可保存的简历数据');
    return;
  }
  await resumeStore.saveCurrentResume(); // store action 处理创建或更新逻辑
  if (resumeStore.error) {
    ElMessage.error(resumeStore.error || '保存失败');
  } else {
    ElMessage.success('简历已保存！');
    // 如果是新创建的简历，后端返回的 resume 对象会包含 id
    // 如果 store 正确更新了 currentResume，路由可能需要更新以包含新的 id
    if (!route.params.id && resumeStore.currentResume?.id) {
      router.replace({ name: 'resumeEdit', params: { id: resumeStore.currentResume.id } });
    }
  }
};

const previewResume = () => {
  // 这里可以实现PDF预览逻辑，例如打开新窗口或使用jsPDF
  ElMessage.info('PDF预览功能待实现');
  // 触发打印 (如果 BasicTemplate 中的打印样式已准备好)
  // window.print(); // 这会打印整个页面，需要调整
};

const goBack = () => {
  router.push({ name: 'home' }); // 或 router.go(-1)
};

// 监听路由参数变化，例如从编辑一个简历切换到编辑另一个简历
watch(() => route.params.id, async (newId, oldId) => {
  if (newId && newId !== oldId && route.name === 'resumeEdit') {
    if (!auth.isAuthenticated) return;
    await resumeStore.fetchResumeById(newId);
     if (resumeStore.error) {
        ElMessage.error(resumeStore.error || '加载简历失败');
    }
  } else if (!newId && route.name === 'resumeNew') { // 从编辑切换到新建
    resumeStore.createNewLocalResume();
  }
});

</script>

<style scoped>
.resume-editor-view {
  height: 100%;
}
.el-container {
  height: calc(100vh - 60px); /* 假设页眉高度为 60px，根据实际 App.vue 调整 */
  display: flex;
  flex-direction: column;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #fff;
  border-bottom: 1px solid #dcdfe6; /* Element Plus 边框颜色 */
  height: auto; /* 调整为 auto 以适应内容 */
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
  box-shadow: none !important; /* 移除输入框默认阴影 */
  border-radius: 0;
}
.resume-title-input :deep(.el-input__inner) {
  border: none !important;
  padding-left: 0;
}

.header-right {
  display: flex;
  gap: 10px;
}

.editor-main-content {
  padding: 0; /* 移除 el-main 的默认内边距，由内部布局控制 */
  overflow: hidden; /* 防止内部滚动条影响布局 */
  flex-grow: 1;
  display: flex; /* 使 editor-layout 能够 flex-grow */
}

.editor-layout {
  display: flex;
  flex-grow: 1;
  width: 100%;
  overflow: hidden; /* 重要：防止子元素溢出 */
}

.editor-pane,
.preview-pane {
  height: 100%; /* 确保占据父容器全部高度 */
  overflow-y: auto; /* 内部滚动 */
  padding: 20px;
  box-sizing: border-box;
}

.editor-pane {
  flex: 1; /* 可以调整比例，例如 flex: 0 0 50%; 或 flex-basis: 50%; */
  background-color: #fff;
  border-right: 1px solid #e0e0e0;
}

.preview-pane {
  flex: 1;
  background-color: #f4f7f9; /* 预览区背景色 */
  display: flex; /* 用于居中预览模板 */
  justify-content: center;
  /* align-items: flex-start; */ /* 如果模板高度不固定 */
}
.preview-wrapper {
    width: 100%;
    /* padding: 1.5rem; */ /* BasicTemplate 自身已有内边距 */
}

.pane-title {
  font-size: 1.25rem;
  font-weight: 500;
  padding-bottom: 10px;
  margin-bottom: 15px;
  border-bottom: 1px solid #e0e0e0;
}
.visually-hidden { /* 用于屏幕阅读器，但视觉上隐藏 */
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
  /* padding: 1.5rem; */ /* editor-pane 已有内边距 */
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
</style>
