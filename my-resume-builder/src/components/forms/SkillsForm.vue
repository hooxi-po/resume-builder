<template>
  <div class="form-section card">
    <h3 class="form-section-title">技能清单</h3>

    <div class="skill-category">
      <h4>技术技能 (例如: JavaScript, Vue.js, Python, SQL)</h4>
      <div v-for="(skill, index) in resume.skills.technical" :key="'tech-' + index" class="skill-item">
        <input type="text" v-model="resume.skills.technical[index]" placeholder="技术技能" />
        <button @click="removeSkill('technical', index)" class="button-remove-inline" aria-label="删除此技能">&times;</button>
      </div>
      <button @click="addSkill('technical')" class="button-add-inline">+ 添加技术技能</button>
    </div>

    <div class="skill-category">
      <h4>语言能力 (例如: 英语 CET-6, 中文 母语)</h4>
      <div v-for="(lang, index) in resume.skills.languages" :key="'lang-' + index" class="skill-item">
        <input type="text" v-model="resume.skills.languages[index]" placeholder="语言及水平" />
        <button @click="removeSkill('languages', index)" class="button-remove-inline" aria-label="删除此语言能力">&times;</button>
      </div>
      <button @click="addSkill('languages')" class="button-add-inline">+ 添加语言能力</button>
    </div>

    <div class="skill-category">
      <h4>软技能 (可选, 例如: 团队合作, 沟通能力, 解决问题)</h4>
      <div v-for="(softSkill, index) in resume.skills.soft" :key="'soft-' + index" class="skill-item">
        <input type="text" v-model="resume.skills.soft[index]" placeholder="软技能" />
        <button @click="removeSkill('soft', index)" class="button-remove-inline" aria-label="删除此技能">&times;</button>
      </div>
      <button @click="addSkill('soft')" class="button-add-inline">+ 添加软技能</button>
    </div>

  </div>
</template>

<script setup>
import { resume } from '../../resumeData';

const addSkill = (category) => {
  if (resume.skills[category] && Array.isArray(resume.skills[category])) {
    resume.skills[category].push(''); // 添加一个空字符串供用户输入
  } else {
    // 如果resume.skills中尚不存在该category，则初始化它
    // 这通常不应该发生，因为resumeData.js中已经定义了结构
    console.warn(`Skill category '${category}' does not exist or is not an array. Initializing.`);
    resume.skills[category] = [''];
  }
};

const removeSkill = (category, index) => {
  if (resume.skills[category] && Array.isArray(resume.skills[category])) {
    resume.skills[category].splice(index, 1);
  }
};
</script>

<style scoped>
@import './formStyles.css';

.skill-category {
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px dashed #eee;
}
.skill-category:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.skill-category h4 {
  font-size: 0.95rem;
  font-weight: 500;
  color: #555;
  margin-bottom: 10px;
}

.skill-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.skill-item input[type="text"] {
  flex-grow: 1;
  margin-right: 8px; /* 输入框和删除按钮之间的间距 */
}

/* .button-add-inline 和 .button-remove-inline 样式已在 formStyles.css 或 ExperienceForm.vue 中定义 */
/* 如果没有，需要从那里复制或确保 formStyles.css 包含它们 */
.button-add-inline {
  background-color: #e8f5e9;
  color: #2e7d32;
  border-color: #a5d6a7;
  margin-top: 5px;
  padding: 6px 10px;
  font-size: 0.85rem;
  border-radius: 4px;
  line-height: 1.2;
  border: 1px solid;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
}
.button-add-inline:hover {
  background-color: #dcedc8;
}

.button-remove-inline {
  background-color: #ffebee;
  color: #c62828;
  border-color: #ef9a9a;
  padding: 8px; /* 调整使其更像一个图标按钮 */
  line-height: 1;
  font-size: 0.85rem; /* 确保和添加按钮大小协调 */
  border-radius: 4px;
  border: 1px solid;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
}
.button-remove-inline:hover {
  background-color: #ffcdd2;
}
</style>
