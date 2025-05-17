// src/resumeData.js
import { reactive } from 'vue';

/**
 * 简历的核心响应式数据对象。
 * 所有表单组件将直接修改这个对象中的数据，
 * 预览组件将读取这个对象中的数据进行展示。
 */
export const resume = reactive({
  personalInfo: {
    name: '', // 姓名
    avatar: '', // 头像 URL (可选)
    title: '', // 当前职位或期望职位，例如 "软件工程师"
    email: '', // 邮箱
    phone: '', // 电话
    linkedin: '', // LinkedIn 个人主页 URL (可选)
    github: '', // GitHub 个人主页 URL (可选)
    website: '', // 个人网站/博客 (可选)
    address: '', // 地址 (可选, 某些模板可能需要)
    city: '', // 城市
    country: '', // 国家
  },
  summary: '', // 自我评价/职业概况
  experience: [
    // 示例:
    // {
    //   id: Date.now(), // 唯一ID，用于v-for的key和删除操作
    //   company: '', // 公司名称
    //   role: '', // 职位
    //   location: '', // 工作地点 (可选)
    //   startDate: '', // 开始日期 (例如 '2020-01' 或 '2020年1月')
    //   endDate: '', // 结束日期 (例如 '2022-12' 或 '至今')
    //   responsibilities: [''], // 职责描述，字符串数组
    //   achievements: [''], // 主要成就 (可选)，字符串数组
    // }
  ],
  education: [
    // 示例:
    // {
    //   id: Date.now(),
    //   school: '', // 学校名称
    //   degree: '', // 学位 (例如 '计算机科学学士')
    //   major: '', // 专业 (可选)
    //   location: '', // 学校所在地 (可选)
    //   startDate: '',
    //   endDate: '',
    //   gpa: '', //绩点 (可选)
    //   description: '', // 补充说明，例如相关课程、荣誉等 (可选)
    // }
  ],
  projects: [
    // 示例:
    // {
    //   id: Date.now(),
    //   name: '', // 项目名称
    //   description: '', // 项目描述
    //   technologies: [''], // 使用的技术栈，字符串数组
    //   url: '', // 项目链接 (可选)
    //   repoUrl: '', // 代码仓库链接 (可选)
    //   startDate: '',
    //   endDate: '',
    // }
  ],
  skills: {
    technical: [''], // 技术技能，例如 'JavaScript', 'Vue.js', 'Node.js'
    languages: [''], // 语言能力，例如 '英语 (流利)', '中文 (母语)'
    soft: [''], // 软技能 (可选), 例如 '团队合作', '沟通能力'
    // 也可以设计成更复杂的结构，例如：
    // skillSet: [
    //   { category: '编程语言', items: ['JavaScript', 'Python'] },
    //   { category: '框架/库', items: ['Vue.js', 'React', 'Node.js'] },
    // ]
  },
  certificates: [
    // 示例:
    // {
    //   id: Date.now(),
    //   name: '', // 证书名称
    //   issuingOrganization: '', // 颁发机构
    //   issueDate: '', // 颁发日期
    //   expirationDate: '', // 失效日期 (可选)
    //   credentialId: '', // 证书ID (可选)
    //   credentialUrl: '' // 证书链接 (可选)
    // }
  ],
  customSections: [ // 用户自定义模块
    // 示例:
    // {
    //   id: Date.now(),
    //   title: '', // 自定义模块标题, 例如 "获奖经历", "志愿者活动"
    //   items: [
    //     {
    //       id: Date.now(),
    //       heading: '', // 小标题或条目名称
    //       subheading: '', // 副标题或日期等
    //       description: '' // 详细描述
    //     }
    //   ]
    // }
  ],
  meta: { // 简历元数据，例如模板选择、颜色主题等，MVP阶段可以简化
    template: 'BasicTemplate', // 当前选择的模板名称
    accentColor: '#007bff', // 主题强调色
    fontFamily: 'Arial, sans-serif', // 字体
  }
});

// --- Helper functions for managing array items (experience, education, etc.) ---
// 这些函数可以直接在组件中使用，或者如果使用Pinia，可以作为actions

/**
 * 向指定的简历模块数组中添加一个新条目。
 * @param {string} sectionKey - 简历数据中的模块键名 (例如 'experience', 'education')。
 * @param {object} newItemTemplate - 新条目的模板对象。
 */
export function addItem(sectionKey, newItemTemplate = {}) {
  if (resume[sectionKey] && Array.isArray(resume[sectionKey])) {
    resume[sectionKey].push({ id: Date.now(), ...newItemTemplate });
  } else {
    console.warn(`Section ${sectionKey} does not exist or is not an array in resume data.`);
  }
}

/**
 * 从指定的简历模块数组中移除一个条目。
 * @param {string} sectionKey - 简历数据中的模块键名。
 * @param {number} itemId - 要移除条目的ID。
 */
export function removeItem(sectionKey, itemId) {
  if (resume[sectionKey] && Array.isArray(resume[sectionKey])) {
    const index = resume[sectionKey].findIndex(item => item.id === itemId);
    if (index !== -1) {
      resume[sectionKey].splice(index, 1);
    }
  } else {
    console.warn(`Section ${sectionKey} does not exist or is not an array in resume data.`);
  }
}

/**
 * 更新指定简历模块数组中特定条目的特定字段。
 * @param {string} sectionKey - 简历数据中的模块键名。
 * @param {number} itemId - 要更新条目的ID。
 * @param {string} fieldKey - 条目中要更新的字段名。
 * @param {*} value - 新的值。
 */
export function updateItemField(sectionKey, itemId, fieldKey, value) {
  if (resume[sectionKey] && Array.isArray(resume[sectionKey])) {
    const item = resume[sectionKey].find(item => item.id === itemId);
    if (item) {
      item[fieldKey] = value;
    }
  } else {
    console.warn(`Section ${sectionKey} does not exist or is not an array in resume data.`);
  }
}

/**
 * 向模块数组中的条目的子数组（例如工作经历的职责列表）添加新项。
 * @param {string} sectionKey - 简历数据中的模块键名 (e.g., 'experience')
 * @param {number} itemId - 父条目的ID
 * @param {string} subArrayKey - 子数组的键名 (e.g., 'responsibilities')
 * @param {string} newItem - 要添加的新项 (通常是字符串)
 */
export function addItemToSubArray(sectionKey, itemId, subArrayKey, newItem = '') {
  if (resume[sectionKey] && Array.isArray(resume[sectionKey])) {
    const item = resume[sectionKey].find(i => i.id === itemId);
    if (item && item[subArrayKey] && Array.isArray(item[subArrayKey])) {
      item[subArrayKey].push(newItem);
    }
  }
}

/**
 * 从模块数组中的条目的子数组中移除项。
 * @param {string} sectionKey
 * @param {number} itemId
 * @param {string} subArrayKey
 * @param {number} subItemIndex - 子数组中要移除项的索引
 */
export function removeItemFromSubArray(sectionKey, itemId, subArrayKey, subItemIndex) {
  if (resume[sectionKey] && Array.isArray(resume[sectionKey])) {
    const item = resume[sectionKey].find(i => i.id === itemId);
    if (item && item[subArrayKey] && Array.isArray(item[subArrayKey])) {
      if (subItemIndex >= 0 && subItemIndex < item[subArrayKey].length) {
        item[subArrayKey].splice(subItemIndex, 1);
      }
    }
  }
}

/**
 * 更新模块数组中条目的子数组中的特定项。
 * @param {string} sectionKey
 * @param {number} itemId
 * @param {string} subArrayKey
 * @param {number} subItemIndex
 * @param {string} value - 新的值
 */
export function updateItemInSubArray(sectionKey, itemId, subArrayKey, subItemIndex, value) {
    if (resume[sectionKey] && Array.isArray(resume[sectionKey])) {
        const item = resume[sectionKey].find(i => i.id === itemId);
        if (item && item[subArrayKey] && Array.isArray(item[subArrayKey])) {
            if (subItemIndex >= 0 && subItemIndex < item[subArrayKey].length) {
                item[subArrayKey][subItemIndex] = value;
            }
        }
    }
}
