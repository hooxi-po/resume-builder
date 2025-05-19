<template>
  <div class="form-section card">
    <h3 class="form-section-title">教育背景</h3>
    <div v-for="(edu, index) in props.resumeData.education" :key="edu.id || index" class="list-item card-nested">
      <div class="item-header">
        <h4>教育经历 #{{ index + 1 }}</h4>
        <button @click="removeEducation(index)" class="button-remove small-button" aria-label="删除此条教育经历">&times; 删除</button>
      </div>
      <div class="grid-container two-columns">
        <div class="form-group">
          <label :for="'school-' + (edu.id || index)">学校名称:</label>
          <input type="text" :id="'school-' + (edu.id || index)" v-model="edu.school" placeholder="例如: XX大学" />
        </div>
        <div class="form-group">
          <label :for="'degree-' + (edu.id || index)">学历/学位:</label>
          <input type="text" :id="'degree-' + (edu.id || index)" v-model="edu.degree" placeholder="例如: 计算机科学学士" />
        </div>
        <div class="form-group">
          <label :for="'major-' + (edu.id || index)">专业 (可选):</label>
          <input type="text" :id="'major-' + (edu.id || index)" v-model="edu.major" placeholder="例如: 软件工程方向" />
        </div>
        <div class="form-group">
          <label :for="'edu-location-' + (edu.id || index)">地点 (可选):</label>
          <input type="text" :id="'edu-location-' + (edu.id || index)" v-model="edu.location" placeholder="例如: 北京" />
        </div>
        <div class="form-group">
          <label :for="'edu-startDate-' + (edu.id || index)">开始日期:</label>
          <input type="text" :id="'edu-startDate-' + (edu.id || index)" v-model="edu.startDate" placeholder="例如: 2016-09 或 2016年9月" />
        </div>
        <div class="form-group">
          <label :for="'edu-endDate-' + (edu.id || index)">结束日期:</label>
          <input type="text" :id="'edu-endDate-' + (edu.id || index)" v-model="edu.endDate" placeholder="例如: 2020-07 或 至今" />
        </div>
        <div class="form-group">
          <label :for="'gpa-' + (edu.id || index)">GPA/成绩 (可选):</label>
          <input type="text" :id="'gpa-' + (edu.id || index)" v-model="edu.gpa" placeholder="例如: 3.8/4.0 或 优秀" />
        </div>
      </div>
      <div class="form-group">
        <label :for="'edu-description-' + (edu.id || index)">补充说明 (可选):</label>
        <textarea :id="'edu-description-' + (edu.id || index)" v-model="edu.description" rows="3" placeholder="例如: 相关课程、荣誉奖项、毕业设计等"></textarea>
      </div>
    </div>
    <button @click="addEducation" class="button-add full-width-button">+ 添加教育经历</button>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

// 修改: 接收 resumeData prop
const props = defineProps({
  resumeData: {
    type: Object,
    required: true
  }
});

// 为新条目生成唯一ID (客户端)
const generateUniqueId = () => {
  return `client_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
};

const addEducation = () => {
  // 确保 props.resumeData.education 是一个数组
  if (!Array.isArray(props.resumeData.education)) {
    props.resumeData.education = [];
  }
  props.resumeData.education.push({
    id: generateUniqueId(), // 添加客户端生成的唯一ID
    school: '',
    degree: '',
    major: '',
    location: '',
    startDate: '',
    endDate: '',
    gpa: '',
    description: '',
  });
};

const removeEducation = (index) => {
  if (props.resumeData.education && props.resumeData.education.length > index) {
    props.resumeData.education.splice(index, 1);
  }
};
</script>

<style scoped>
@import './formStyles.css'; /* 引入共享表单样式 */

.list-item {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px dashed #e0e0e0;
}
.list-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}
.card-nested {
  background-color: #fdfdfd;
  padding: 15px;
  border: 1px solid #f0f0f0;
  border-radius: 6px;
}
.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}
.item-header h4 {
  margin: 0;
  font-size: 1rem;
  font-weight: 500;
}
/* 确保 two-columns 和 form-group 样式已在 formStyles.css 或此处定义 */
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
.form-group label {
  margin-bottom: 5px;
  font-weight: 500;
  font-size: 0.9em;
}
.form-group input[type="text"],
.form-group textarea {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9em;
  width: 100%;
  box-sizing: border-box;
}
@media (max-width: 768px) {
  .two-columns {
    grid-template-columns: 1fr;
  }
}
</style>
