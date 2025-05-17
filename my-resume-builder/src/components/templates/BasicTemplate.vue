<template>
  <div class="resume-preview-basic" :style="templateStyles">
    <div class="preview-content" id="resume-content-to-print">
      <header class="resume-section personal-info-section">
        <div class="info-main">
          <h1 class="name">{{ resumeData.personalInfo.name || '你的姓名' }}</h1>
          <p class="title" v-if="resumeData.personalInfo.title">{{ resumeData.personalInfo.title }}</p>
        </div>
        <div class="contact-info">
          <p v-if="resumeData.personalInfo.email"><span class="icon">📧</span> {{ resumeData.personalInfo.email }}</p>
          <p v-if="resumeData.personalInfo.phone"><span class="icon">📞</span> {{ resumeData.personalInfo.phone }}</p>
          <p v-if="resumeData.personalInfo.city || resumeData.personalInfo.country">
            <span class="icon">📍</span>
            {{ [resumeData.personalInfo.city, resumeData.personalInfo.country].filter(Boolean).join(', ') }}
          </p>
          <p v-if="resumeData.personalInfo.linkedin"><span class="icon">🔗</span> <a :href="formatUrl(resumeData.personalInfo.linkedin)" target="_blank" rel="noopener noreferrer">LinkedIn</a></p>
          <p v-if="resumeData.personalInfo.github"><span class="icon">💻</span> <a :href="formatUrl(resumeData.personalInfo.github)" target="_blank" rel="noopener noreferrer">GitHub</a></p>
          <p v-if="resumeData.personalInfo.website"><span class="icon">🌐</span> <a :href="formatUrl(resumeData.personalInfo.website)" target="_blank" rel="noopener noreferrer">个人网站</a></p>
        </div>
         <div v-if="resumeData.personalInfo.avatar" class="avatar-container">
          <img :src="resumeData.personalInfo.avatar" alt="个人头像" class="avatar-image" />
        </div>
      </header>

      <section class="resume-section summary-section" v-if="resumeData.summary">
        <h2 class="section-title">自我评价</h2>
        <p class="summary-text">{{ resumeData.summary }}</p>
      </section>

      <section class="resume-section experience-section" v-if="resumeData.experience && resumeData.experience.length">
        <h2 class="section-title">工作经历</h2>
        <div v-for="exp in resumeData.experience" :key="exp.id" class="entry">
          <div class="entry-header">
            <h3 class="entry-title">{{ exp.role || '职位' }} <span class="at-company">@ {{ exp.company || '公司名称' }}</span></h3>
            <p class="entry-dates">{{ exp.startDate || '开始日期' }} – {{ exp.endDate || '结束日期' }}</p>
          </div>
          <p class="entry-location" v-if="exp.location">{{ exp.location }}</p>
          <ul class="details-list" v-if="exp.responsibilities && exp.responsibilities.some(r => r.trim() !== '')">
            <li v-for="(resp, rIndex) in exp.responsibilities.filter(r => r.trim() !== '')" :key="'resp-' + exp.id + '-' + rIndex">{{ resp }}</li>
          </ul>
          <h4 class="sub-heading" v-if="exp.achievements && exp.achievements.some(a => a.trim() !== '')">主要成就:</h4>
          <ul class="details-list achievements-list" v-if="exp.achievements && exp.achievements.some(a => a.trim() !== '')">
            <li v-for="(ach, aIndex) in exp.achievements.filter(a => a.trim() !== '')" :key="'ach-' + exp.id + '-' + aIndex">{{ ach }}</li>
          </ul>
        </div>
      </section>

      <section class="resume-section education-section" v-if="resumeData.education && resumeData.education.length">
        <h2 class="section-title">教育背景</h2>
        <div v-for="edu in resumeData.education" :key="edu.id" class="entry">
          <div class="entry-header">
            <h3 class="entry-title">{{ edu.degree || '学位' }} <span v-if="edu.major">- {{ edu.major }}</span></h3>
            <p class="entry-dates">{{ edu.startDate || '开始日期' }} – {{ edu.endDate || '结束日期' }}</p>
          </div>
          <p class="entry-institution">{{ edu.school || '学校名称' }} <span v-if="edu.location">, {{ edu.location }}</span></p>
          <p class="entry-gpa" v-if="edu.gpa">GPA: {{ edu.gpa }}</p>
          <p class="entry-description" v-if="edu.description">{{ edu.description }}</p>
        </div>
      </section>

      <section class="resume-section projects-section" v-if="resumeData.projects && resumeData.projects.length">
        <h2 class="section-title">项目经历</h2>
        <div v-for="proj in resumeData.projects" :key="proj.id" class="entry">
          <div class="entry-header">
            <h3 class="entry-title">{{ proj.name || '项目名称' }}</h3>
            <p class="entry-dates" v-if="proj.startDate || proj.endDate">{{ proj.startDate }} – {{ proj.endDate }}</p>
          </div>
          <p class="entry-description" v-if="proj.description">{{ proj.description }}</p>
          <p class="tech-stack" v-if="proj.technologies && proj.technologies.length">
            <strong>技术栈:</strong> {{ proj.technologies.join(', ') }}
          </p>
          <p class="project-links">
            <a v-if="proj.url" :href="formatUrl(proj.url)" target="_blank" rel="noopener noreferrer">[项目链接]</a>
            <a v-if="proj.repoUrl" :href="formatUrl(proj.repoUrl)" target="_blank" rel="noopener noreferrer">[代码仓库]</a>
          </p>
        </div>
      </section>

      <section class="resume-section skills-section" v-if="hasSkills">
        <h2 class="section-title">技能清单</h2>
        <div class="skills-grid">
            <div class="skill-category-display" v-if="resumeData.skills.technical && resumeData.skills.technical.some(s => s.trim() !== '')">
                <h4 class="skill-category-title">技术技能</h4>
                <ul class="skills-list">
                <li v-for="(skill, index) in resumeData.skills.technical.filter(s => s.trim() !== '')" :key="'tech-' + index">{{ skill }}</li>
                </ul>
            </div>
            <div class="skill-category-display" v-if="resumeData.skills.languages && resumeData.skills.languages.some(s => s.trim() !== '')">
                <h4 class="skill-category-title">语言能力</h4>
                <ul class="skills-list">
                <li v-for="(lang, index) in resumeData.skills.languages.filter(s => s.trim() !== '')" :key="'lang-' + index">{{ lang }}</li>
                </ul>
            </div>
            <div class="skill-category-display" v-if="resumeData.skills.soft && resumeData.skills.soft.some(s => s.trim() !== '')">
                <h4 class="skill-category-title">软技能</h4>
                <ul class="skills-list">
                <li v-for="(soft, index) in resumeData.skills.soft.filter(s => s.trim() !== '')" :key="'soft-' + index">{{ soft }}</li>
                </ul>
            </div>
        </div>
      </section>

      <section class="resume-section certificates-section" v-if="resumeData.certificates && resumeData.certificates.length">
        <h2 class="section-title">证书</h2>
        <div v-for="cert in resumeData.certificates" :key="cert.id" class="entry">
          <div class="entry-header">
            <h3 class="entry-title">{{ cert.name || '证书名称' }}</h3>
            <p class="entry-dates" v-if="cert.issueDate">{{ cert.issueDate }} <span v-if="cert.expirationDate"> – {{ cert.expirationDate }}</span></p>
          </div>
          <p class="entry-institution" v-if="cert.issuingOrganization">颁发机构: {{ cert.issuingOrganization }}</p>
          <p v-if="cert.credentialId">ID: {{ cert.credentialId }}</p>
          <p v-if="cert.credentialUrl"><a :href="formatUrl(cert.credentialUrl)" target="_blank" rel="noopener noreferrer">[查看证书]</a></p>
        </div>
      </section>

      <section class="resume-section custom-section" v-for="custom in resumeData.customSections" :key="custom.id">
        <h2 class="section-title">{{ custom.title || '自定义模块' }}</h2>
        <div v-for="item in custom.items" :key="item.id" class="entry">
          <h3 class="entry-title" v-if="item.heading">{{ item.heading }}</h3>
          <p class="entry-dates" v-if="item.subheading">{{ item.subheading }}</p>
          <p class="entry-description" v-if="item.description">{{ item.description }}</p>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  resumeData: {
    type: Object,
    required: true
  }
});

// 确保URL以http(s)://开头
const formatUrl = (url) => {
  if (!url) return '#';
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    return 'http://' + url;
  }
  return url;
};

// 检查是否有任何技能被填写
const hasSkills = computed(() => {
  const skills = props.resumeData.skills;
  if (!skills) return false;
  return (skills.technical && skills.technical.some(s => s.trim() !== '')) ||
         (skills.languages && skills.languages.some(s => s.trim() !== '')) ||
         (skills.soft && skills.soft.some(s => s.trim() !== ''));
});

// 从 resumeData.meta 获取模板样式 (MVP阶段可以简化或硬编码)
const templateStyles = computed(() => {
  const meta = props.resumeData.meta || {};
  return {
    '--accent-color': meta.accentColor || '#007bff', // 默认强调色
    'font-family': meta.fontFamily || 'Arial, Helvetica, sans-serif', // 默认字体
    // 可以在这里添加更多CSS变量，如主文本颜色、背景色等
  };
});

</script>

<style scoped>
/* BasicTemplate.vue specific styles */
.resume-preview-basic {
  background-color: #ffffff;
  color: #333333;
  /* 使用CSS变量来应用动态样式 */
  font-family: var(--font-family, 'Roboto', sans-serif); /* 默认字体 */
  padding: 30px 25px; /* A4纸张的典型边距感 */
  margin: auto; /* 在预览区域内居中显示 */
  width: 100%; /* 宽度由父容器 .preview-wrapper 控制 */
  max-width: 800px; /* 模拟A4宽度，可以调整 */
  min-height: calc(800px * 1.414); /* 模拟A4高度比例 */
  box-shadow: 0 0 15px rgba(0,0,0,0.1);
  border-radius: 3px;
  line-height: 1.6;
}

.preview-content {
  /* 此元素的内容将被打印 */
}

.resume-section {
  margin-bottom: 20px;
}
.resume-section:last-child {
  margin-bottom: 0;
}

.section-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--accent-color, #0056b3); /* 使用强调色 */
  border-bottom: 2px solid var(--accent-color, #0056b3);
  padding-bottom: 6px;
  margin-bottom: 15px;
  text-transform: uppercase; /* 可选：标题大写 */
  letter-spacing: 0.5px; /* 可选：轻微字间距 */
}

/* 个人信息头部 */
.personal-info-section {
  display: grid;
  grid-template-areas:
    "main avatar"
    "contact avatar";
  grid-template-columns: 1fr auto; /* 联系信息占满，头像自适应 */
  gap: 10px 20px;
  padding-bottom: 15px;
  margin-bottom: 25px;
  border-bottom: 1px solid #eee;
  align-items: center; /* 垂直居中对齐 */
}
.info-main {
  grid-area: main;
}
.contact-info {
  grid-area: contact;
  font-size: 0.9rem;
}
.avatar-container {
  grid-area: avatar;
  justify-self: end; /* 头像靠右 */
  align-self: start; /* 头像从顶部开始 */
}
.avatar-image {
  width: 100px; /* 可调整 */
  height: 100px;
  border-radius: 50%; /* 圆形头像 */
  object-fit: cover; /* 保持图片比例 */
  border: 2px solid var(--accent-color, #0056b3);
}

.personal-info-section .name {
  font-size: 2.2rem;
  font-weight: 700;
  margin: 0 0 5px 0;
  color: #222;
}
.personal-info-section .title {
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--accent-color, #0056b3);
  margin: 0 0 10px 0;
}
.contact-info p {
  margin: 3px 0;
  display: flex;
  align-items: center;
}
.contact-info .icon {
  margin-right: 8px;
  color: var(--accent-color, #0056b3);
  font-size: 1rem;
}
.contact-info a {
  color: #333;
  text-decoration: none;
}
.contact-info a:hover {
  color: var(--accent-color, #0056b3);
  text-decoration: underline;
}

/* 自我评价 */
.summary-text {
  font-size: 0.95rem;
  white-space: pre-wrap; /* 保留换行和空格 */
}

/* 通用条目样式 (工作经历, 教育背景等) */
.entry {
  margin-bottom: 18px;
}
.entry:last-child {
  margin-bottom: 0;
}

.entry-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline; /* 标题和日期基线对齐 */
  margin-bottom: 3px;
}
.entry-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
  color: #444;
}
.entry-title .at-company, .entry-title .degree-major {
  font-weight: normal;
  color: #555;
}
.entry-dates {
  font-size: 0.85rem;
  color: #666;
  font-style: italic;
  white-space: nowrap; /* 防止日期换行 */
}
.entry-institution, .entry-location, .entry-gpa {
  font-size: 0.9rem;
  margin: 2px 0;
  color: #555;
}
.entry-description {
  font-size: 0.9rem;
  margin: 5px 0;
  white-space: pre-wrap;
}
.sub-heading { /* 例如 "主要成就:" */
    font-size: 0.95rem;
    font-weight: bold;
    margin-top: 8px;
    margin-bottom: 4px;
    color: #444;
}

.details-list {
  list-style-type: disc; /* 实心圆点 */
  padding-left: 20px;
  margin: 5px 0 10px 0;
  font-size: 0.9rem;
}
.details-list li {
  margin-bottom: 4px;
}
.achievements-list {
    /* list-style-type: '🏆 '; /* 可以用 emoji 或其他符号，但兼容性需注意 */
}


/* 项目经历特定样式 */
.tech-stack {
  font-size: 0.85rem;
  margin: 5px 0;
}
.tech-stack strong {
  font-weight: 600;
}
.project-links a {
  font-size: 0.85rem;
  margin-right: 10px;
  color: var(--accent-color, #0056b3);
  text-decoration: none;
}
.project-links a:hover {
  text-decoration: underline;
}


/* 技能清单 */
.skills-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); /* 响应式列 */
    gap: 20px;
}
.skill-category-display {
    /* padding: 10px; border: 1px solid #eee; border-radius: 4px; */
}
.skill-category-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: #444;
}
.skills-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-wrap: wrap; /* 技能项换行 */
  gap: 8px; /* 技能项之间的间距 */
}
.skills-list li {
  background-color: #f0f0f0; /* 浅灰色背景 */
  color: #444;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 0.85rem;
  /* border: 1px solid var(--accent-color, #0056b3); */ /* 可选边框 */
}

/* 打印样式 */
@media print {
  body {
    margin: 0;
    padding: 0;
    background-color: #fff; /* 确保打印背景为白色 */
    -webkit-print-color-adjust: exact; /* Chrome, Safari, Edge - 强制打印背景色和图片 */
    print-color-adjust: exact; /* Firefox - 强制打印背景色和图片 */
  }
  .resume-preview-basic {
    width: 100% !important;
    max-width: none !important;
    min-height: unset !important;
    margin: 0 !important;
    padding: 20mm 15mm 20mm 20mm; /* 典型打印边距: 上 右 下 左 */
    box-shadow: none !important;
    border-radius: 0 !important;
    border: none !important;
    font-size: 10pt; /* 调整打印字体大小 */
    color: #000 !important; /* 确保文本为黑色 */
  }
  .section-title {
    color: #000 !important; /* 打印时标题也用黑色，除非设计需要 */
    border-bottom-color: #000 !important;
  }
  .personal-info-section .name {
     color: #000 !important;
  }
  .personal-info-section .title,
  .contact-info .icon,
  .contact-info a:hover {
    color: #000 !important; /* 打印时链接和强调色也用黑色 */
  }
  .contact-info a {
    text-decoration: none; /* 打印时通常不显示下划线 */
    color: #000 !important;
  }
  .avatar-image {
    border-color: #000 !important; /* 头像边框 */
  }
  .skills-list li {
    background-color: #f0f0f0 !important; /* 确保打印背景 */
    color: #000 !important;
    border: 1px solid #ccc !important; /* 打印时给技能标签加个边框可能更好看 */
  }
  /* 隐藏不需要打印的链接文本 (例如 [项目链接] ) */
  a[href]:after {
    /* content: " (" attr(href) ")"; */ /* 可选：打印时显示URL */
    /* font-size: 0.8em; */
    /* color: #555; */
  }
  /* 避免分页符打断内容 */
  .resume-section, .entry {
    page-break-inside: avoid;
  }
  h1, h2, h3, h4, h5, h6 {
    page-break-after: avoid;
  }
  ul, ol, p {
    page-break-before: avoid;
  }
}
</style>
