<template>
  <div class="form-section card">
    <h3 class="form-section-title">个人信息</h3>
    <div class="grid-container two-columns">
      <div class="form-group">
        <label for="name">姓名:</label>
        <input type="text" id="name" v-model="props.resumeData.personalInfo.name" placeholder="例如: 张三" />
      </div>
      <div class="form-group">
        <label for="title">职位/称谓:</label>
        <input type="text" id="title" v-model="props.resumeData.personalInfo.title" placeholder="例如: 软件工程师" />
      </div>
      <div class="form-group">
        <label for="email">邮箱:</label>
        <input type="email" id="email" v-model="props.resumeData.personalInfo.email" placeholder="your.email@example.com" />
      </div>
      <div class="form-group">
        <label for="phone">电话:</label>
        <input type="tel" id="phone" v-model="props.resumeData.personalInfo.phone" placeholder="13800138000" />
      </div>
      <div class="form-group">
        <label for="city">城市:</label>
        <input type="text" id="city" v-model="props.resumeData.personalInfo.city" placeholder="例如: 上海" />
      </div>
      <div class="form-group">
        <label for="country">国家:</label>
        <input type="text" id="country" v-model="props.resumeData.personalInfo.country" placeholder="例如: 中国" />
      </div>
        <div class="form-group full-width">
        <label for="address">详细地址 (可选):</label>
        <input type="text" id="address" v-model="props.resumeData.personalInfo.address" placeholder="例如: XX区XX路XX号" />
      </div>
      <div class="form-group">
        <label for="linkedin">LinkedIn (可选):</label>
        <input type="url" id="linkedin" v-model="props.resumeData.personalInfo.linkedin" placeholder="https://linkedin.com/in/yourprofile" />
      </div>
      <div class="form-group">
        <label for="github">GitHub (可选):</label>
        <input type="url" id="github" v-model="props.resumeData.personalInfo.github" placeholder="https://github.com/yourusername" />
      </div>
      <div class="form-group full-width">
        <label for="website">个人网站/博客 (可选):</label>
        <input type="url" id="website" v-model="props.resumeData.personalInfo.website" placeholder="https://your.website.com" />
      </div>
      <div class="form-group full-width">
        <label for="avatar">头像链接 (可选, URL):</label>
        <input type="url" id="avatar" v-model="props.resumeData.personalInfo.avatar" placeholder="https://example.com/avatar.jpg" />
      </div>
    </div>
    <div class="form-group">
      <label for="summary">自我评价/职业概况:</label>
      <textarea id="summary" v-model="props.resumeData.summary" rows="4" placeholder="简要介绍您的核心竞争力、职业目标等..."></textarea>
    </div>
  </div>
</template>

<script setup>
// 修改: 移除本地 resume 导入，改为接收 prop
const props = defineProps({
  resumeData: {
    type: Object,
    required: true
  }
});

// 现在，模板中的 v-model="props.resumeData.personalInfo.name" 等
// 将会直接修改从 ResumeEditorView 传递过来的、来自 Pinia store 的响应式对象。
</script>

<style scoped>
/* 样式保持不变 */
.card {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.form-section-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-top: 0;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.grid-container {
  display: grid;
  gap: 15px;
}

.two-columns {
  grid-template-columns: repeat(2, 1fr);
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1; /* 占据整行 */
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #454545;
}

.form-group input[type="text"],
.form-group input[type="email"],
.form-group input[type="tel"],
.form-group input[type="url"],
.form-group textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #dcdcdc;
  border-radius: 6px;
  font-size: 0.9rem;
  box-sizing: border-box;
  transition: border-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.2);
  outline: none;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

@media (max-width: 768px) {
  .two-columns {
    grid-template-columns: 1fr;
  }
}
</style>
