<template>
  <div class="form-section card">
    <h3 class="form-section-title">工作经历</h3>
    <div v-for="(exp, index) in resume.experience" :key="exp.id" class="list-item card-nested">
      <div class="item-header">
        <h4>工作经历 #{{ index + 1 }}</h4>
        <button @click="removeExperience(exp.id)" class="button-remove small-button" aria-label="删除此条工作经历">&times; 删除</button>
      </div>
      <div class="grid-container two-columns">
        <div class="form-group">
          <label :for="'company-' + exp.id">公司名称:</label>
          <input type="text" :id="'company-' + exp.id" v-model="exp.company" placeholder="例如: XX科技有限公司" />
        </div>
        <div class="form-group">
          <label :for="'role-' + exp.id">职位:</label>
          <input type="text" :id="'role-' + exp.id" v-model="exp.role" placeholder="例如: 前端开发工程师" />
        </div>
        <div class="form-group">
          <label :for="'exp-location-' + exp.id">工作地点 (可选):</label>
          <input type="text" :id="'exp-location-' + exp.id" v-model="exp.location" placeholder="例如: 远程 或 上海市" />
        </div>
        <div class="form-group">
          <label :for="'exp-startDate-' + exp.id">开始日期:</label>
          <input type="text" :id="'exp-startDate-' + exp.id" v-model="exp.startDate" placeholder="例如: 2020-01" />
        </div>
        <div class="form-group">
          <label :for="'exp-endDate-' + exp.id">结束日期:</label>
          <input type="text" :id="'exp-endDate-' + exp.id" v-model="exp.endDate" placeholder="例如: 2022-12 或 至今" />
        </div>
      </div>

      <div class="form-group">
        <label :for="'responsibilities-' + exp.id">主要职责 (每点一行):</label>
        <div v-for="(resp, rIndex) in exp.responsibilities" :key="rIndex" class="sub-list-item">
          <textarea
            :id="'responsibility-' + exp.id + '-' + rIndex"
            v-model="exp.responsibilities[rIndex]"
            rows="2"
            placeholder="例如: 负责XX模块的开发与维护 (使用STAR法则描述更佳)"
          ></textarea>
          <button @click="removeResponsibility(exp.id, rIndex)" class="button-remove-inline" aria-label="删除此条职责">&times;</button>
        </div>
        <button @click="addResponsibility(exp.id)" class="button-add-inline">+ 添加职责</button>
      </div>

       <div class="form-group">
        <label :for="'achievements-' + exp.id">主要成就 (可选, 每点一行):</label>
        <div v-for="(ach, aIndex) in exp.achievements" :key="aIndex" class="sub-list-item">
          <textarea
            :id="'achievement-' + exp.id + '-' + aIndex"
            v-model="exp.achievements[aIndex]"
            rows="2"
            placeholder="例如: 优化了XX流程，效率提升20%"
          ></textarea>
          <button @click="removeAchievement(exp.id, aIndex)" class="button-remove-inline" aria-label="删除此条成就">&times;</button>
        </div>
        <button @click="addAchievement(exp.id)" class="button-add-inline">+ 添加成就</button>
      </div>
    </div>
    <button @click="addExperience" class="button-add full-width-button">+ 添加工作经历</button>
  </div>
</template>

<script setup>
import { resume, addItem, removeItem, addItemToSubArray, removeItemFromSubArray, updateItemInSubArray } from '../../resumeData';

const addExperience = () => {
  const newExperienceTemplate = {
    company: '',
    role: '',
    location: '',
    startDate: '',
    endDate: '',
    responsibilities: [''], // 默认带一个空的职责输入框
    achievements: [''], // 默认带一个空的成就输入框
  };
  addItem('experience', newExperienceTemplate);
};

const removeExperience = (id) => {
  removeItem('experience', id);
};

// --- Responsibilities ---
const addResponsibility = (experienceId) => {
  addItemToSubArray('experience', experienceId, 'responsibilities', '');
};

const removeResponsibility = (experienceId, responsibilityIndex) => {
  removeItemFromSubArray('experience', experienceId, 'responsibilities', responsibilityIndex);
};
// 如果需要实时更新子数组中的项，可以像下面这样（但v-model通常直接工作）
// const updateResponsibility = (experienceId, responsibilityIndex, event) => {
//   updateItemInSubArray('experience', experienceId, 'responsibilities', responsibilityIndex, event.target.value);
// };

// --- Achievements ---
const addAchievement = (experienceId) => {
  addItemToSubArray('experience', experienceId, 'achievements', '');
};

const removeAchievement = (experienceId, achievementIndex) => {
  removeItemFromSubArray('experience', experienceId, 'achievements', achievementIndex);
};
</script>

<style scoped>
@import './formStyles.css';

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

.sub-list-item {
  display: flex;
  align-items: flex-start; /* 文本域可能多行，按钮顶部对齐 */
  margin-bottom: 8px;
}
.sub-list-item textarea {
  flex-grow: 1;
  margin-right: 8px; /* 文本域和删除按钮之间的间距 */
}

.button-add-inline, .button-remove-inline {
  padding: 6px 10px;
  font-size: 0.85rem;
  border-radius: 4px;
  line-height: 1.2; /* 确保文字垂直居中 */
  border: 1px solid;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
}
.button-add-inline {
  background-color: #e8f5e9; /* 淡绿色背景 */
  color: #2e7d32; /* 深绿色文字 */
  border-color: #a5d6a7; /* 浅绿色边框 */
  margin-top: 5px; /* 与上方元素的间距 */
}
.button-add-inline:hover {
  background-color: #dcedc8;
}

.button-remove-inline {
  background-color: #ffebee; /* 淡红色背景 */
  color: #c62828; /* 深红色文字 */
  border-color: #ef9a9a; /* 浅红色边框 */
  padding: 8px; /* 调整使其更像一个图标按钮 */
  line-height: 1;
}
.button-remove-inline:hover {
  background-color: #ffcdd2;
}
</style>
