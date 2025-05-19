<template>
  <div class="home-view-styled">
    <div class="page-title-bar">
      <h1 class="page-main-title">我的简历</h1>
      <el-button type="primary" :icon="Plus" @click="createNewResume" round size="large">
        创建新简历
      </el-button>
    </div>

    <div v-if="resumeStore.isLoading" class="loading-state">
      <el-skeleton :rows="6" animated />
    </div>
    <div v-else-if="resumeStore.error" class="error-state">
      <el-alert :title="resumeStore.error" type="error" show-icon :closable="false" />
      <el-button @click="retryFetchResumes" style="margin-top: 15px;">重试</el-button>
    </div>
    <div v-else-if="!resumeStore.userResumes || resumeStore.userResumes.length === 0" class="empty-state-container">
      <el-empty description="您还没有创建任何简历，开始创建您的第一份吧！">
        <el-button type="primary" @click="createNewResume" size="large" :icon="EditPen">
          立即创建第一份简历
        </el-button>
      </el-empty>
    </div>
    <div v-else class="resume-grid">
      <el-card
        v-for="resume in resumeStore.userResumes"
        :key="resume._id" class="resume-card-styled"
        shadow="hover"
      >
        <template #header>
          <div class="card-header-content">
            <span class="resume-card-title">{{ resume.resume_name }}</span>
            <el-dropdown @command="(command) => handleCommand(command, resume._id)" trigger="click"> <el-button text :icon="MoreFilled" class="more-actions-trigger" aria-label="更多操作"></el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="edit" :icon="Edit">编辑</el-dropdown-item>
                  <el-dropdown-item command="preview" :icon="View" disabled>预览</el-dropdown-item>
                  <el-dropdown-item command="delete" :icon="Delete" divided class="delete-dropdown-item">删除</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </template>
        <div class="resume-card-body-content">
          <p class="resume-detail-item">
            <el-icon><Opportunity /></el-icon>
            职位: {{ resume.resume_data?.personalInfo?.title || '未指定' }}
          </p>
          <p class="resume-detail-item last-updated-styled">
            <el-icon><Clock /></el-icon>
            最后更新: {{ formatDate(resume.updated_at) }}
          </p>
        </div>
        <template #footer>
          <el-button type="primary" plain @click="editResume(resume._id)" class="edit-button-full" round> <el-icon style="margin-right: 5px;"><EditPen /></el-icon>
            打开编辑器
          </el-button>
        </template>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
// 使用相对路径导入 store
import { useAuthStore } from '../stores/authStore.js';
import { useResumeStore } from '../stores/resumeStore.js';
import { useRouter } from 'vue-router';
// 按需导入 Element Plus 组件和图标
import { 
  ElMessage, ElMessageBox, ElButton, ElCard, 
  ElSkeleton, ElAlert, ElEmpty, ElDropdown, 
  ElDropdownMenu, ElDropdownItem, ElIcon 
} from 'element-plus';
import { Plus, MoreFilled, Edit, View, Delete, Opportunity, Clock, EditPen } from '@element-plus/icons-vue';

const auth = useAuthStore();
const resumeStore = useResumeStore();
const router = useRouter();

onMounted(() => {
  if (auth.isAuthenticated) {
    resumeStore.fetchUserResumes();
  }
});

const createNewResume = () => {
  router.push({ name: 'resumeNew' });
};

const editResume = (resumeId) => { // resumeId 应该是 _id
  if (!resumeId) {
    ElMessage.error('无法编辑简历：ID 未定义。');
    return;
  }
  router.push({ name: 'resumeEdit', params: { id: resumeId } });
};

const deleteResume = async (resumeId) => { // resumeId 应该是 _id
  if (!resumeId) {
    ElMessage.error('无法删除简历：ID 未定义。');
    return;
  }
  try {
    await ElMessageBox.confirm(
      '确定要删除这份简历吗？此操作无法撤销。',
      '警告',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
        draggable: true, // Element Plus 2.2.0+
      }
    );
    await resumeStore.deleteResume(resumeId); // 确保 store 的 deleteResume 使用的是 _id
    ElMessage.success('简历删除成功');
  } catch (error) {
    // ElMessageBox.confirm 在用户点击取消或关闭时会 reject 一个字符串 "cancel" 或 "close"
    if (error !== 'cancel' && error !== 'close') {
      console.info("用户取消删除或删除过程中发生错误:", error);
    } else {
      ElMessage.info('已取消删除');
    }
  }
};

const handleCommand = (command, resumeId) => { // resumeId 应该是 _id
  if (!resumeId && (command === 'edit' || command === 'delete' || command === 'preview')) {
      ElMessage.error(`操作失败：简历ID未定义。`);
      return;
  }
  if (command === 'edit') {
    editResume(resumeId);
  } else if (command === 'delete') {
    deleteResume(resumeId);
  } else if (command === 'preview') {
    ElMessage.info('预览功能待实现');
  }
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  try {
    const date = new Date(dateString);
    // 检查日期是否有效
    if (isNaN(date.getTime())) {
      return '无效日期';
    }
    return date.toLocaleDateString(undefined, { 
      year: 'numeric', month: '2-digit', day: '2-digit', 
      hour: '2-digit', minute: '2-digit' 
    });
  } catch (e) {
    console.error("Error formatting date:", e);
    return '日期格式错误';
  }
};

const retryFetchResumes = () => {
    if (auth.isAuthenticated) {
        resumeStore.fetchUserResumes();
    } else {
        ElMessage.warning("请先登录后再重试。");
    }
};
</script>

<style scoped>
.home-view-styled {
  padding: 25px 30px; 
  background-color: #f8f9fa; 
  min-height: calc(100vh - 60px - 70px); /* 假设头部60px, 页脚70px, 根据实际情况调整 */
}

.page-title-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px; 
  padding-bottom: 20px; 
  border-bottom: 1px solid #dee2e6; 
}

.page-main-title {
  font-size: 2.25rem; 
  font-weight: 700;
  color: #212529; 
  margin: 0;
}

.loading-state,
.error-state,
.empty-state-container {
  margin-top: 50px; 
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 20px;
}
.error-state .el-button {
  margin-top: 20px; 
}

.resume-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); 
  gap: 25px; 
}

.resume-card-styled {
  border-radius: 10px; 
  transition: transform 0.25s ease-in-out, box-shadow 0.25s ease-in-out;
  display: flex;
  flex-direction: column;
  background-color: #fff; 
}

.resume-card-styled:hover {
  transform: translateY(-6px); 
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08); 
}

.card-header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.resume-card-title {
  font-size: 1.3rem; 
  font-weight: 600;
  color: #343a40; 
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-right: 10px;
}

.more-actions-trigger.el-button { 
  padding: 6px;
  border-radius: 50%;
  font-size: 1.1rem; 
}
.more-actions-trigger.el-button:hover {
  background-color: #f1f3f5; 
}

.resume-card-body-content {
  font-size: 0.95rem; 
  color: #495057; 
  line-height: 1.7; 
  flex-grow: 1;
  padding: 15px 0 10px 0; 
}

.resume-detail-item {
  display: flex;
  align-items: center;
  gap: 10px; 
  margin-bottom: 10px; 
}
.resume-detail-item .el-icon {
  color: #6c757d; 
  font-size: 1.1em; 
}

.last-updated-styled {
  font-size: 0.85rem; 
  color: #6c757d;
}

.edit-button-full.el-button { 
  width: 100%;
  font-weight: 500;
  padding-top: 12px; 
  padding-bottom: 12px;
  font-size: 0.95rem;
}
.edit-button-full.el-button .el-icon {
  margin-right: 6px;
}

.delete-dropdown-item { 
  color: var(--el-color-danger) !important;
}
.delete-dropdown-item:hover,
.delete-dropdown-item:focus {
  background-color: var(--el-color-danger-light-9) !important;
  color: var(--el-color-danger) !important;
}

.empty-state-container .el-button {
  font-size: 1rem;
  padding: 12px 24px;
}
.empty-state-container .el-empty {
    padding-bottom: 20px; 
}
</style>
