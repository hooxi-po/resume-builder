<template>
  <div class="form-section card">
    <h3 class="form-section-title">工作经历</h3>
    <div v-for="(exp, index) in props.resumeData.experience" :key="exp.id || index" class="list-item card-nested">
      <div class="item-header">
        <h4>工作经历 #{{ index + 1 }}</h4>
        <button @click="removeExperience(index)" class="button-remove small-button" aria-label="删除此条工作经历">&times; 删除</button>
      </div>
      <div class="grid-container two-columns">
        <div class="form-group">
          <label :for="'company-' + (exp.id || index)">公司名称:</label>
          <input type="text" :id="'company-' + (exp.id || index)" v-model="exp.company" placeholder="例如: XX科技有限公司" />
        </div>
        <div class="form-group">
          <label :for="'role-' + (exp.id || index)">职位:</label>
          <input type="text" :id="'role-' + (exp.id || index)" v-model="exp.role" placeholder="例如: 前端开发工程师" />
        </div>
        <div class="form-group">
          <label :for="'exp-location-' + (exp.id || index)">工作地点 (可选):</label>
          <input type="text" :id="'exp-location-' + (exp.id || index)" v-model="exp.location" placeholder="例如: 远程 或 上海市" />
        </div>
        <div class="form-group">
          <label :for="'exp-startDate-' + (exp.id || index)">开始日期:</label>
          <input type="text" :id="'exp-startDate-' + (exp.id || index)" v-model="exp.startDate" placeholder="例如: 2020-01" />
        </div>
        <div class="form-group">
          <label :for="'exp-endDate-' + (exp.id || index)">结束日期:</label>
          <input type="text" :id="'exp-endDate-' + (exp.id || index)" v-model="exp.endDate" placeholder="例如: 2022-12 或 至今" />
        </div>
      </div>

      <div class="form-group">
        <label :for="'responsibilities-' + (exp.id || index)">主要职责 (每点一行):</label>
        <div v-for="(resp, rIndex) in exp.responsibilities" :key="rIndex" class="sub-list-item">
          <textarea
            :id="'responsibility-' + (exp.id || index) + '-' + rIndex"
            v-model="exp.responsibilities[rIndex]" rows="2"
            placeholder="例如: 负责XX模块的开发与维护 (使用STAR法则描述更佳)"
          ></textarea>
          <button @click="removeResponsibility(index, rIndex)" class="button-remove-inline" aria-label="删除此条职责">&times;</button>
        </div>
        <button @click="addResponsibility(index)" class="button-add-inline">+ 添加职责</button>
      </div>

      <div class="form-group">
        <label :for="'achievements-' + (exp.id || index)">主要成就 (可选, 每点一行):</label>
        <div v-for="(ach, aIndex) in exp.achievements" :key="aIndex" class="sub-list-item">
          <textarea
            :id="'achievement-' + (exp.id || index) + '-' + aIndex"
            v-model="exp.achievements[aIndex]" rows="2"
            placeholder="例如: 优化了XX流程，效率提升20%"
          ></textarea>
          <button @click="removeAchievement(index, aIndex)" class="button-remove-inline" aria-label="删除此条成就">&times;</button>
        </div>
        <button @click="addAchievement(index)" class="button-add-inline">+ 添加成就</button>
      </div>
    </div>
    <button @click="addExperience" class="button-add full-width-button">+ 添加工作经历</button>
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

const addExperience = () => {
  if (!Array.isArray(props.resumeData.experience)) {
    props.resumeData.experience = [];
  }
  props.resumeData.experience.push({
    id: generateUniqueId(),
    company: '',
    role: '',
    location: '',
    startDate: '',
    endDate: '',
    responsibilities: [''], // 默认带一个空的职责输入框
    achievements: [''],   // 默认带一个空的成就输入框
  });
};

const removeExperience = (experienceIndex) => {
  if (props.resumeData.experience && props.resumeData.experience.length > experienceIndex) {
    props.resumeData.experience.splice(experienceIndex, 1);
  }
};

// --- Responsibilities ---
const addResponsibility = (experienceIndex) => {
  const exp = props.resumeData.experience[experienceIndex];
  if (exp) {
    if (!Array.isArray(exp.responsibilities)) {
      exp.responsibilities = [];
    }
    exp.responsibilities.push('');
  }
};

const removeResponsibility = (experienceIndex, responsibilityIndex) => {
  const exp = props.resumeData.experience[experienceIndex];
  if (exp && exp.responsibilities && exp.responsibilities.length > responsibilityIndex) {
    exp.responsibilities.splice(responsibilityIndex, 1);
  }
};

// --- Achievements ---
const addAchievement = (experienceIndex) => {
  const exp = props.resumeData.experience[experienceIndex];
  if (exp) {
    if (!Array.isArray(exp.achievements)) {
      exp.achievements = [];
    }
    exp.achievements.push('');
  }
};

const removeAchievement = (experienceIndex, achievementIndex) => {
  const exp = props.resumeData.experience[experienceIndex];
  if (exp && exp.achievements && exp.achievements.length > achievementIndex) {
    exp.achievements.splice(achievementIndex, 1);
  }
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
  align-items: flex-start;
  margin-bottom: 8px;
}
.sub-list-item textarea {
  flex-grow: 1;
  margin-right: 8px;
}

.button-add-inline, .button-remove-inline {
  padding: 6px 10px;
  font-size: 0.85rem;
  border-radius: 4px;
  line-height: 1.2;
  border: 1px solid;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
}
.button-add-inline {
  background-color: #e8f5e9;
  color: #2e7d32;
  border-color: #a5d6a7;
  margin-top: 5px;
}
.button-add-inline:hover {
  background-color: #dcedc8;
}

.button-remove-inline {
  background-color: #ffebee;
  color: #c62828;
  border-color: #ef9a9a;
  padding: 8px;
  line-height: 1;
}
.button-remove-inline:hover {
  background-color: #ffcdd2;
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
