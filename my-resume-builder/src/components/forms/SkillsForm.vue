<template>
  <div class="form-section card">
    <h3 class="form-section-title">技能清单</h3>

    <div class="skill-category">
      <h4>技术技能 (例如: JavaScript, Vue.js, Python, SQL)</h4>
      <div v-for="(skill, index) in props.resumeData.skills.technical" :key="'tech-' + index" class="skill-item">
        <input type="text" v-model="props.resumeData.skills.technical[index]" placeholder="技术技能" />
        <button @click="removeSkill('technical', index)" class="button-remove-inline" aria-label="删除此技能">&times;</button>
      </div>
      <button @click="addSkill('technical')" class="button-add-inline">+ 添加技术技能</button>
    </div>

    <div class="skill-category">
      <h4>语言能力 (例如: 英语 CET-6, 中文 母语)</h4>
      <div v-for="(lang, index) in props.resumeData.skills.languages" :key="'lang-' + index" class="skill-item">
        <input type="text" v-model="props.resumeData.skills.languages[index]" placeholder="语言及水平" />
        <button @click="removeSkill('languages', index)" class="button-remove-inline" aria-label="删除此语言能力">&times;</button>
      </div>
      <button @click="addSkill('languages')" class="button-add-inline">+ 添加语言能力</button>
    </div>

    <div class="skill-category">
      <h4>软技能 (可选, 例如: 团队合作, 沟通能力, 解决问题)</h4>
      <div v-for="(softSkill, index) in props.resumeData.skills.soft" :key="'soft-' + index" class="skill-item">
        <input type="text" v-model="props.resumeData.skills.soft[index]" placeholder="软技能" />
        <button @click="removeSkill('soft', index)" class="button-remove-inline" aria-label="删除此技能">&times;</button>
      </div>
      <button @click="addSkill('soft')" class="button-add-inline">+ 添加软技能</button>
    </div>

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

const addSkill = (category) => {
  // 确保 props.resumeData.skills 对象存在且对应类别是数组
  if (props.resumeData.skills && props.resumeData.skills[category]) {
    if (!Array.isArray(props.resumeData.skills[category])) {
      props.resumeData.skills[category] = []; // 如果不是数组，则初始化为空数组
    }
    props.resumeData.skills[category].push(''); // 添加一个空字符串供用户输入
  } else if (props.resumeData.skills) {
    // 如果 skills 对象存在但类别不存在，则创建该类别数组
    props.resumeData.skills[category] = [''];
    console.warn(`Skill category '${category}' was not an array. Initialized.`);
  } else {
    // 如果 skills 对象本身不存在 (理论上不应该，因为 store 中有默认结构)
    props.resumeData.skills = { [category]: [''] };
    console.warn(`Skills object or category '${category}' did not exist. Initialized.`);
  }
};

const removeSkill = (category, index) => {
  if (props.resumeData.skills &&
      props.resumeData.skills[category] &&
      Array.isArray(props.resumeData.skills[category]) &&
      props.resumeData.skills[category].length > index) {
    props.resumeData.skills[category].splice(index, 1);
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
  margin-right: 8px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.9em;
  box-sizing: border-box;
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
</style>
