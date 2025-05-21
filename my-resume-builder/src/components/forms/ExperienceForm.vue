<template>
  <div class="form-section card">
    <h3 class="form-section-title">工作经历</h3>

    <!-- New Textarea for Job Description/Keywords -->
    <div class="form-group">
      <label for="job-context-text">职位描述/相关关键词 (用于AI建议):</label>
      <textarea
        id="job-context-text"
        v-model="jobContextText"
        rows="3"
        placeholder="在此粘贴职位描述或输入相关技能关键词，以便AI提供更精准的建议。"
        class="full-width-input"
      ></textarea>
    </div>

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
        <div class="ai-suggestion-controls">
          <button @click="fetchAISuggestions(exp, 'responsibility', rIndex)" class="button-ai-suggestion small-button">✨ 获取AI建议</button>
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
        <div class="ai-suggestion-controls">
          <button @click="fetchAISuggestions(exp, 'achievement', aIndex)" class="button-ai-suggestion small-button">✨ 获取AI建议</button>
        </div>
        <button @click="addAchievement(index)" class="button-add-inline">+ 添加成就</button>
      </div>
    </div>
    <button @click="addExperience" class="button-add full-width-button">+ 添加工作经历</button>

    <!-- AI Suggestion Modal -->
    <div v-if="showSuggestionModal" class="modal-backdrop">
      <div class="modal-content">
        <h3>AI 建议</h3>
        <p v-if="suggestionTarget && suggestionTarget.originalText">
          <strong>原内容:</strong> {{ suggestionTarget.originalText }}
        </p>
        <div v-if="currentSuggestions.length > 0">
          <ul>
            <li v-for="(suggestion, sIndex) in currentSuggestions" :key="sIndex" class="suggestion-item">
              <p><strong>建议 {{ sIndex + 1 }}:</strong> {{ suggestion.suggested_text }}</p>
              <p v-if="suggestion.explanation"><em>说明: {{ suggestion.explanation }}</em></p>
              <button @click="applySuggestion(suggestion.suggested_text)" class="button-primary small-button">应用此建议</button>
            </li>
          </ul>
        </div>
        <p v-else>
          AI 未能提供建议或返回空建议。
        </p>
        <button @click="closeSuggestionModal" class="button-secondary full-width-button">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, ref } from 'vue';
import { getAIContentSuggestions } from '../../services/api'; // Import the API function

// Reactive variable for job context text
const jobContextText = ref('');

// State for AI Suggestions Modal
const currentSuggestions = ref([]);
const suggestionTarget = ref(null); // Will store { experienceItem, fieldType, index, originalText }
const showSuggestionModal = ref(false);


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

// --- AI Suggestions ---
const closeSuggestionModal = () => {
  showSuggestionModal.value = false;
  currentSuggestions.value = [];
  suggestionTarget.value = null;
};

const applySuggestion = (suggestionText) => {
  if (suggestionTarget.value) {
    const { experienceItem, fieldType, itemIndex } = suggestionTarget.value;
    if (fieldType === 'responsibility') {
      experienceItem.responsibilities[itemIndex] = suggestionText;
    } else if (fieldType === 'achievement') {
      experienceItem.achievements[itemIndex] = suggestionText;
    }
    closeSuggestionModal();
  }
};

const fetchAISuggestions = async (experienceItem, fieldType, itemIndex) => { // Renamed 'index' to 'itemIndex' for clarity
  // Clear previous suggestions and close modal if already open for a different target
  if (showSuggestionModal.value) {
    closeSuggestionModal();
  }

  if (!jobContextText.value.trim()) {
    alert('请输入职位描述或相关关键词，以便AI提供建议。');
    return;
  }

  let currentText = '';
  let sectionType = '';
  const sectionData = {
    for_role: experienceItem.role,
    for_company: experienceItem.company,
  };

  if (fieldType === 'responsibility') {
    currentText = experienceItem.responsibilities[itemIndex];
    sectionType = 'experience_responsibility';
    sectionData.current_text = currentText;
  } else if (fieldType === 'achievement') {
    currentText = experienceItem.achievements[itemIndex];
    sectionType = 'experience_achievement';
    sectionData.current_text = currentText;
  } else {
    console.error("Invalid fieldType for AI suggestion:", fieldType);
    return;
  }

  if (!currentText.trim()) {
    alert(`请输入当前的${fieldType === 'responsibility' ? '职责' : '成就'}内容，以便AI提供建议。`);
    return;
  }

  const requestPayload = {
    section_data: sectionData,
    context_text: jobContextText.value,
    section_type: sectionType,
  };

  console.log("Sending AI Suggestion Request:", JSON.stringify(requestPayload, null, 2));

  try {
    const response = await getAIContentSuggestions(requestPayload);
    console.log("AI Suggestion Response:", response);

    if (response && response.suggestions) {
      currentSuggestions.value = response.suggestions;
      suggestionTarget.value = { experienceItem, fieldType, itemIndex, originalText: currentText };
      showSuggestionModal.value = true;
    } else {
      currentSuggestions.value = [];
      suggestionTarget.value = null; // Clear target if no suggestions
      alert("AI 未能提供建议或返回空建议。");
    }
  } catch (error) {
    console.error("Error fetching AI suggestions:", error);
    currentSuggestions.value = [];
    suggestionTarget.value = null;
    alert("获取AI建议失败，请查看控制台了解详情。");
  }
};
</script>

<style scoped>
@import './formStyles.css';

/* Modal Styles */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* Ensure it's on top */
}

.modal-content {
  background-color: #fff;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
  width: 90%;
  max-width: 600px; /* Max width for the modal */
  max-height: 80vh; /* Max height */
  overflow-y: auto; /* Scroll if content overflows */
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 1.4rem;
  color: #333;
}

.modal-content ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.suggestion-item {
  border: 1px solid #eee;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 6px;
  background-color: #f9f9f9;
}

.suggestion-item p {
  margin-top: 0;
  margin-bottom: 8px;
  font-size: 0.95rem;
}
.suggestion-item p strong {
 color: #555;
}
.suggestion-item em {
  font-size: 0.85rem;
  color: #777;
}

.suggestion-item button {
  margin-top: 10px;
  margin-right: 5px; /* Spacing for buttons if multiple are added */
}

.modal-content .button-secondary {
  margin-top: 20px;
  background-color: #6c757d;
  border-color: #6c757d;
  color: white;
}
.modal-content .button-secondary:hover {
  background-color: #5a6268;
  border-color: #545b62;
}

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

.full-width-input {
  width: 100%;
  box-sizing: border-box; /* Ensures padding doesn't expand it beyond 100% */
}

.ai-suggestion-controls {
  margin-top: 5px;
  margin-bottom: 10px; /* Add some space before "add" button */
  text-align: left; /* Align button to the left */
}
.button-ai-suggestion {
  background-color: #e3f2fd; /* Light blue */
  color: #0d47a1; /* Dark blue */
  border-color: #90caf9;
  padding: 6px 10px;
  font-size: 0.85rem;
  border-radius: 4px;
  line-height: 1.2;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s;
}
.button-ai-suggestion:hover {
  background-color: #bbdefb;
}

/* Ensure small-button and full-width-button styles are available or define them */
.small-button {
  padding: 6px 12px;
  font-size: 0.875rem;
}
.full-width-button {
  width: 100%;
  padding: 10px;
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
