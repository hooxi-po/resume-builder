<template>
  <div class="home-view">
    <el-container v-if="auth.isAuthenticated">
      <el-header class="page-header">
        <h1>我的简历</h1>
        <el-button type="primary" icon="Plus" @click="createNewResume" round>
          创建新简历
        </el-button>
      </el-header>
      <el-main>
        <div v-if="resumeStore.isLoading" class="loading-state">
          <el-skeleton :rows="5" animated />
        </div>
        <div v-else-if="resumeStore.error" class="error-state">
          <el-alert :title="resumeStore.error" type="error" show-icon :closable="false" />
        </div>
        <div v-else-if="resumeStore.userResumes.length === 0" class="empty-state">
          <el-empty description="您还没有创建任何简历">
            <el-button type="primary" @click="createNewResume" size="large">立即创建第一份简历</el-button>
          </el-empty>
        </div>
        <div v-else class="resume-list">
          <el-row :gutter="20">
            <el-col
              v-for="resume in resumeStore.userResumes"
              :key="resume.id"
              :xs="24" :sm="12" :md="8" :lg="6"
            >
              <el-card class="resume-card" shadow="hover">
                <template #header>
                  <div class="resume-card-header">
                    <span class="resume-name">{{ resume.resume_name }}</span>
                    <el-dropdown @command="(command) => handleCommand(command, resume.id)">
                      <el-button type="primary" link icon="MoreFilled" class="more-actions-button" />
                      <template #dropdown>
                        <el-dropdown-menu>
                          <el-dropdown-item command="edit" icon="Edit">编辑</el-dropdown-item>
                          <el-dropdown-item command="preview" icon="View">预览 (待实现)</el-dropdown-item>
                          <el-dropdown-item command="delete" icon="Delete" divided class="delete-item">删除</el-dropdown-item>
                        </el-dropdown-menu>
                      </template>
                    </el-dropdown>
                  </div>
                </template>
                <div class="resume-card-body">
                  <p class="last-updated">
                    最后更新: {{ formatDate(resume.updated_at) }}
                  </p>
                  <p class="resume-details-placeholder">
                    {{ resume.resume_data?.personalInfo?.title || '暂无职位信息' }}
                  </p>
                </div>
                <template #footer>
                   <el-button type="primary" plain @click="editResume(resume.id)" class="full-width-button" round>
                     打开编辑器
                   </el-button>
                </template>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </el-main>
    </el-container>
    <div v-else>
      <p>请先 <router-link :to="{ name: 'login' }">登录</router-link> 以查看您的简历。</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useAuthStore } from '/home/leven/24-25/resume-builder/my-resume-builder/src/stores/authStore.js';
import { useResumeStore } from '/home/leven/24-25/resume-builder/my-resume-builder/src/stores/resumeStore'; // 假设您已创建 resumeStore
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus'; // 用于消息提示和确认框

const auth = useAuthStore();
const resumeStore = useResumeStore();
const router = useRouter();

onMounted(() => {
  if (auth.isAuthenticated) {
    resumeStore.fetchUserResumes();
  }
});

const createNewResume = () => {
  // resumeStore.createNewLocalResume(); // 在 store 中初始化一个空的本地简历对象
  router.push({ name: 'resumeNew' }); // 跳转到新建简历的路由
};

const editResume = (resumeId) => {
  router.push({ name: 'resumeEdit', params: { id: resumeId } });
};

const deleteResume = async (resumeId) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这份简历吗？此操作无法撤销。',
      '警告',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
      }
    );
    // 用户点击了确定
    await resumeStore.deleteResume(resumeId);
    ElMessage({
      type: 'success',
      message: '简历删除成功',
    });
  } catch (error) {
    // 用户点击了取消或关闭对话框，或者删除过程中发生错误
    if (error !== 'cancel' && error !== 'close') {
        // ElMessage({ type: 'error', message: resumeStore.error || '删除失败' });
        console.error("删除简历时发生错误或用户取消:", error);
    } else {
        ElMessage({ type: 'info', message: '已取消删除' });
    }
  }
};

const handleCommand = (command, resumeId) => {
  if (command === 'edit') {
    editResume(resumeId);
  } else if (command === 'delete') {
    deleteResume(resumeId);
  } else if (command === 'preview') {
    ElMessage.info('预览功能待实现');
    // router.push({ name: 'resumePreview', params: { id: resumeId } }); // 假设有预览路由
  }
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};
</script>

<style scoped>
.home-view {
  padding: 0; /* 通常视图本身不需要内边距，由内部 el-container 控制 */
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #ebeef5; /* Element Plus 分割线颜色 */
  background-color: #fff;
  margin-bottom: 20px;
}
.page-header h1 {
  margin: 0;
  font-size: 1.8rem;
  color: #303133;
}

.loading-state, .error-state, .empty-state {
  padding: 20px;
  text-align: center;
}

.resume-list {
  padding: 0 20px; /* 给列表一些左右内边距 */
}

.resume-card {
  margin-bottom: 20px;
  border-radius: 8px;
  transition: box-shadow 0.3s ease-in-out;
}
.resume-card:hover {
  box-shadow: var(--el-box-shadow-dark);
}

.resume-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.resume-name {
  font-weight: bold;
  font-size: 1.1rem;
  color: #303133;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: calc(100% - 40px); /* 给右侧按钮留空间 */
}
.more-actions-button {
  padding: 5px; /* 使图标按钮点击区域更大一些 */
  font-size: 1.2rem; /* 增大图标 */
}
.el-dropdown-menu__item.delete-item {
  color: var(--el-color-danger);
}
.el-dropdown-menu__item.delete-item:hover {
  background-color: var(--el-color-danger-light-9);
  color: var(--el-color-danger);
}


.resume-card-body {
  font-size: 0.9rem;
  color: #606266;
  min-height: 60px; /* 给内容一些最小高度 */
}
.last-updated {
  font-size: 0.8rem;
  color: #909399; /* Element Plus 提示文字颜色 */
  margin-bottom: 8px;
}
.resume-details-placeholder {
  /* 样式用于占位符文本 */
}
.full-width-button {
  width: 100%;
}
</style>
