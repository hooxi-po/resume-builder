<template>
  <div class="login-view">
    <LoginForm />
  </div>
</template>

<script setup>
// 从 components 文件夹导入 LoginForm 组件
// 路径 ../components/ 表示从当前 views 文件夹返回上一级到 src，然后再进入 components
import LoginForm from '../components/LoginForm.vue';
</script>

<style scoped>
.login-view {
  /* 您可以在这里为登录视图添加特定的布局样式，如果需要的话 */
  /* 例如，确保 LoginForm 在页面中垂直和水平居中 */
  display: flex;
  justify-content: center;
  align-items: flex-start; /* 或者 center，取决于您希望如何对齐 */
  padding-top: 20px; /* 给顶部一些空间 */
  min-height: calc(100vh - 120px); /* 减去页眉和页脚的大致高度 */
}
</style>
