<template>
  <div class="not-found-view">
    <el-result
      icon="error"
      title="404 - 页面未找到"
      sub-title="抱歉，您访问的页面不存在或已被移除。"
    >
      <template #extra>
        <el-button type="primary" @click="goHome">返回首页</el-button>
      </template>
    </el-result>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const goHome = () => {
  router.push({ name: 'home' }); // 假设您的首页路由名称为 'home'
};
</script>

<style scoped>
.not-found-view {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 120px); /* 减去页眉和页脚的大致高度 */
  padding: 20px;
}
/* 可以根据需要调整 el-result 组件的样式 */
</style>
