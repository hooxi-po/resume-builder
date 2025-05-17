<template>
  <div class="app-container">
    <header class="app-header">
      <h1>简历生成器 MVP</h1>
      <p class="app-subtitle">实时编辑，即时预览</p>
    </header>

    <main class="main-content">
      <section class="editor-pane">
        <h2 class="pane-title">编辑简历内容</h2>
        <div class="form-sections-container">
          <PersonalInfoForm />
          <EducationForm />
          <ExperienceForm />
          <SkillsForm />
          </div>
      </section>

      <section class="preview-pane">
        <h2 class="pane-title">简历预览</h2>
        <div class="preview-wrapper">
          <BasicTemplate :resumeData="resume" />
        </div>
      </section>
    </main>

    <footer class="app-footer">
      <button @click="exportToJson" class="action-button">导出为 JSON</button>
      <button @click="printPreview" class="action-button">打印/另存为 PDF</button>
      <p class="footer-note">© 2025 简历生成器</p>
    </footer>
  </div>
</template>

<script setup>
// 导入共享的响应式简历数据
// 假设 resumeData.js 使用 Vue 的 reactive 创建并导出了 resume 对象
// 如果使用 Pinia，则从 store 中导入
import { resume } from './resumeData';

// 导入表单组件
import PersonalInfoForm from './components/forms/PersonalInfoForm.vue';
import EducationForm from './components/forms/EducationForm.vue';
import ExperienceForm from './components/forms/ExperienceForm.vue';
import SkillsForm from './components/forms/SkillsForm.vue'; // 新增技能表单

// 导入预览模板组件
import BasicTemplate from './components/templates/BasicTemplate.vue';

// 导出简历数据为 JSON 文件
const exportToJson = () => {
  // 使用 toRaw 获取 resume 代理对象的原始对象，避免导出 Vue 的内部属性
  // 如果 resume 不是 proxy (例如直接从 Pinia store 获取的普通对象)，可以不用 toRaw
  // const rawResumeData = toRaw(resume); // 如果 resume 是 proxy
  const dataStr = JSON.stringify(resume, null, 2); // 使用 resume，假设它是普通JS对象或Pinia state
  const dataUri = 'data:application/json;charset=utf-8,' + encodeURIComponent(dataStr);
  const exportFileDefaultName = 'my_resume.json';

  const linkElement = document.createElement('a');
  linkElement.setAttribute('href', dataUri);
  linkElement.setAttribute('download', exportFileDefaultName);
  document.body.appendChild(linkElement); // 需要添加到DOM中才能触发点击 (在某些浏览器中)
  linkElement.click();
  document.body.removeChild(linkElement); // 清理
};

// 触发浏览器打印功能，用户可以选择“另存为PDF”
// 这依赖于 BasicTemplate.vue 中定义的 @media print 样式
const printPreview = () => {
  window.print();
};
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: #f4f7f9; /* 淡雅的背景色 */
  color: #333;
}

.app-header {
  background-color: #ffffff; /* 白色头部 */
  color: #2c3e50; /* 深色文字 */
  padding: 1.5rem 2rem;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); /* 轻微阴影 */
  border-bottom: 1px solid #e0e0e0;
}

.app-header h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: 600;
}

.app-subtitle {
  margin: 0.25rem 0 0;
  font-size: 0.9rem;
  color: #555;
}

.main-content {
  display: flex;
  flex-grow: 1;
  padding: 1.5rem; /* 主内容区内边距 */
  gap: 1.5rem; /* 编辑区和预览区之间的间距 */
  overflow: hidden; /* 防止子元素溢出导致滚动条 */
}

.editor-pane,
.preview-pane {
  background-color: #ffffff;
  border-radius: 8px; /* 圆角 */
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 确保子元素滚动 */
}

.editor-pane {
  flex: 1; /* 编辑区占据更多空间或等分 */
  min-width: 400px; /* 最小宽度，防止过窄 */
}

.preview-pane {
  flex: 1; /* 预览区占据空间，可以调整比例，例如 flex: 0 0 45%; */
  min-width: 400px; /* 最小宽度 */
  /* 如果希望预览区有固定A4比例，需要更复杂的CSS或JS计算 */
}

.pane-title {
  font-size: 1.25rem;
  font-weight: 500;
  padding: 1rem 1.5rem;
  margin: 0;
  background-color: #f9fafb; /* 标题栏背景色 */
  border-bottom: 1px solid #e0e0e0;
}

.form-sections-container {
  padding: 1.5rem;
  overflow-y: auto; /* 使表单内容可滚动 */
  flex-grow: 1; /* 占据剩余空间 */
}

.preview-wrapper {
  padding: 1.5rem; /* 预览内容的外边距 */
  overflow-y: auto; /* 使预览内容可滚动 */
  flex-grow: 1;
  background-color: #e8edf0; /* 预览区域的背景，使其与模板区分 */
  display: flex; /* 用于居中模板 */
  justify-content: center; /* 水平居中 */
  /* align-items: flex-start;  如果模板高度不固定，从顶部开始 */
}

/* BasicTemplate 组件本身应该有自己的背景色和尺寸控制 */
/* 例如 .preview-wrapper > div { margin: auto; } 可以帮助居中模板 */


.app-footer {
  background-color: #ffffff;
  padding: 1rem 2rem;
  text-align: center;
  border-top: 1px solid #e0e0e0;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.05);
}

.action-button {
  background-color: #007bff; /* 主题蓝色 */
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease-in-out, transform 0.1s ease;
  margin: 0 0.5rem;
}

.action-button:hover {
  background-color: #0056b3; /* 深一点的蓝色 */
}

.action-button:active {
  transform: translateY(1px);
}

.footer-note {
  margin-top: 1rem;
  font-size: 0.8rem;
  color: #777;
}

/* 响应式调整 */
@media (max-width: 992px) { /* 中等屏幕，例如平板 */
  .main-content {
    flex-direction: column;
    padding: 1rem;
    gap: 1rem;
  }
  .editor-pane,
  .preview-pane {
    min-width: unset; /* 移除最小宽度限制 */
    max-height: 70vh; /* 限制高度，避免过长 */
  }
  .preview-wrapper {
     align-items: flex-start; /* 小屏幕时，预览内容从顶部开始 */
  }
}

@media (max-width: 768px) { /* 小型屏幕，例如手机 */
  .app-header h1 {
    font-size: 1.5rem;
  }
  .app-subtitle {
    font-size: 0.8rem;
  }
  .pane-title {
    font-size: 1.1rem;
    padding: 0.75rem 1rem;
  }
  .form-sections-container,
  .preview-wrapper {
    padding: 1rem;
  }
  .action-button {
    padding: 0.6rem 1.2rem;
    font-size: 0.85rem;
  }
}
</style>
