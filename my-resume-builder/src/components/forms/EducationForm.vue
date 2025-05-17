<template>
  <div class="form-section card">
    <h3 class="form-section-title">教育背景</h3>
    <div v-for="(edu, index) in resume.education" :key="edu.id" class="list-item card-nested">
      <div class="item-header">
        <h4>教育经历 #{{ index + 1 }}</h4>
        <button @click="removeEducation(edu.id)" class="button-remove small-button" aria-label="删除此条教育经历">&times; 删除</button>
      </div>
      <div class="grid-container two-columns">
        <div class="form-group">
          <label :for="'school-' + edu.id">学校名称:</label>
          <input type="text" :id="'school-' + edu.id" v-model="edu.school" placeholder="例如: XX大学" />
        </div>
        <div class="form-group">
          <label :for="'degree-' + edu.id">学历/学位:</label>
          <input type="text" :id="'degree-' + edu.id" v-model="edu.degree" placeholder="例如: 计算机科学学士" />
        </div>
        <div class="form-group">
          <label :for="'major-' + edu.id">专业 (可选):</label>
          <input type="text" :id="'major-' + edu.id" v-model="edu.major" placeholder="例如: 软件工程方向" />
        </div>
        <div class="form-group">
          <label :for="'edu-location-' + edu.id">地点 (可选):</label>
          <input type="text" :id="'edu-location-' + edu.id" v-model="edu.location" placeholder="例如: 北京" />
        </div>
        <div class="form-group">
          <label :for="'edu-startDate-' + edu.id">开始日期:</label>
          <input type="text" :id="'edu-startDate-' + edu.id" v-model="edu.startDate" placeholder="例如: 2016-09 或 2016年9月" />
        </div>
        <div class="form-group">
          <label :for="'edu-endDate-' + edu.id">结束日期:</label>
          <input type="text" :id="'edu-endDate-' + edu.id" v-model="edu.endDate" placeholder="例如: 2020-07 或 至今" />
        </div>
        <div class="form-group">
          <label :for="'gpa-' + edu.id">GPA/成绩 (可选):</label>
          <input type="text" :id="'gpa-' + edu.id" v-model="edu.gpa" placeholder="例如: 3.8/4.0 或 优秀" />
        </div>
      </div>
      <div class="form-group">
        <label :for="'edu-description-' + edu.id">补充说明 (可选):</label>
        <textarea :id="'edu-description-' + edu.id" v-model="edu.description" rows="3" placeholder="例如: 相关课程、荣誉奖项、毕业设计等"></textarea>
      </div>
    </div>
    <button @click="addEducation" class="button-add full-width-button">+ 添加教育经历</button>
  </div>
</template>

<script setup>
import { resume, addItem, removeItem } from '../../resumeData';

const addEducation = () => {
  // 提供一个新教育经历条目的模板
  const newEducationTemplate = {
    school: '',
    degree: '',
    major: '',
    location: '',
    startDate: '',
    endDate: '',
    gpa: '',
    description: '',
  };
  addItem('education', newEducationTemplate);
};

const removeEducation = (id) => {
  removeItem('education', id);
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
.card-nested { /* 用于列表项内部的卡片感，如果需要的话 */
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
</style>
