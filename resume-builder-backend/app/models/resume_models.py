# app/models/resume_models.py
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

# --- 子模块的模型 ---
class PersonalInfo(BaseModel):
    name: Optional[str] = Field(None, example="张三")
    avatar: Optional[HttpUrl] = Field(None, example="https://example.com/avatar.jpg")
    title: Optional[str] = Field(None, example="软件工程师")
    email: Optional[str] = Field(None, example="zhangsan@example.com") # 可以是EmailStr，但前端可能不强制
    phone: Optional[str] = Field(None, example="13800138000")
    linkedin: Optional[HttpUrl] = Field(None, example="https://linkedin.com/in/zhangsan")
    github: Optional[HttpUrl] = Field(None, example="https://github.com/zhangsan")
    website: Optional[HttpUrl] = Field(None, example="https://zhangsan.com")
    address: Optional[str] = Field(None, example="XX区XX路XX号")
    city: Optional[str] = Field(None, example="上海")
    country: Optional[str] = Field(None, example="中国")

class ExperienceItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    company: Optional[str] = Field(None, example="XX科技有限公司")
    role: Optional[str] = Field(None, example="前端开发工程师")
    location: Optional[str] = Field(None, example="上海市")
    startDate: Optional[str] = Field(None, example="2020-01")
    endDate: Optional[str] = Field(None, example="2022-12 或 至今")
    responsibilities: Optional[List[str]] = Field(default_factory=list, example=["负责XX模块的开发与维护"])
    achievements: Optional[List[str]] = Field(default_factory=list, example=["优化XX流程，效率提升20%"])

class EducationItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    school: Optional[str] = Field(None, example="XX大学")
    degree: Optional[str] = Field(None, example="计算机科学学士")
    major: Optional[str] = Field(None, example="软件工程")
    location: Optional[str] = Field(None, example="北京")
    startDate: Optional[str] = Field(None, example="2016-09")
    endDate: Optional[str] = Field(None, example="2020-07")
    gpa: Optional[str] = Field(None, example="3.8/4.0")
    description: Optional[str] = Field(None, example="相关课程：数据结构、算法分析")

class ProjectItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: Optional[str] = Field(None, example="个人博客系统")
    description: Optional[str] = Field(None, example="基于Vue和FastAPI的个人博客")
    technologies: Optional[List[str]] = Field(default_factory=list, example=["Vue.js", "FastAPI", "MongoDB"])
    url: Optional[HttpUrl] = Field(None, example="https://myblog.com")
    repoUrl: Optional[HttpUrl] = Field(None, example="https://github.com/user/myblog")
    startDate: Optional[str] = Field(None, example="2023-01")
    endDate: Optional[str] = Field(None, example="2023-05")

class Skills(BaseModel):
    technical: Optional[List[str]] = Field(default_factory=list, example=["JavaScript", "Python", "Vue.js"])
    languages: Optional[List[str]] = Field(default_factory=list, example=["英语 (流利)", "中文 (母语)"])
    soft: Optional[List[str]] = Field(default_factory=list, example=["团队合作", "沟通能力"])

class CertificateItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: Optional[str] = Field(None, example="AWS解决方案架构师认证")
    issuingOrganization: Optional[str] = Field(None, example="Amazon Web Services")
    issueDate: Optional[str] = Field(None, example="2022-08")
    expirationDate: Optional[str] = Field(None, example="2025-08")
    credentialId: Optional[str] = Field(None, example="AWS123456XYZ")
    credentialUrl: Optional[HttpUrl] = Field(None, example="https://aw.cert/validate/123")

class CustomSectionItemDetail(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    heading: Optional[str] = Field(None, example="XX编程竞赛一等奖")
    subheading: Optional[str] = Field(None, example="2019年全国大学生程序设计竞赛")
    description: Optional[str] = Field(None, example="团队负责人，主要负责算法设计与实现。")

class CustomSectionItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: Optional[str] = Field(None, example="获奖经历")
    items: Optional[List[CustomSectionItemDetail]] = Field(default_factory=list)

class ResumeMeta(BaseModel):
    template: Optional[str] = Field("BasicTemplate", example="ModernTemplate")
    accentColor: Optional[str] = Field("#007bff", example="#FF5733")
    fontFamily: Optional[str] = Field("Arial, sans-serif", example="Roboto, sans-serif")

# --- 简历主模型 ---
class ResumeData(BaseModel): # 这个模型对应前端的 resume 响应式对象
    personalInfo: PersonalInfo = Field(default_factory=PersonalInfo)
    summary: Optional[str] = Field(None, example="一位经验丰富的软件工程师...")
    experience: List[ExperienceItem] = Field(default_factory=list)
    education: List[EducationItem] = Field(default_factory=list)
    projects: List[ProjectItem] = Field(default_factory=list)
    skills: Skills = Field(default_factory=Skills)
    certificates: List[CertificateItem] = Field(default_factory=list)
    customSections: List[CustomSectionItem] = Field(default_factory=list)
    meta: ResumeMeta = Field(default_factory=ResumeMeta)

class ResumeBase(BaseModel):
    resume_name: str = Field(..., example="我的第一份技术简历")
    # resume_data 结构与前端的 resume 对象一致
    # 使用 Any 类型可以提供最大的灵活性，但失去了类型检查的优势
    # 或者直接使用上面定义的 ResumeData 模型
    resume_data: ResumeData = Field(default_factory=ResumeData)

class ResumeCreate(ResumeBase):
    pass

class ResumeUpdate(BaseModel):
    resume_name: Optional[str] = None
    resume_data: Optional[ResumeData] = None # 允许部分更新或完整替换

class ResumeInDB(ResumeBase):
    id: str = Field(alias="_id") # MongoDB 使用 _id
    user_id: str = Field(...) # 关联到用户
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        # Pydantic V2:
        # from_attributes = True
        # Pydantic V1:
        orm_mode = True

class Resume(ResumeInDB): # 返回给客户端的模型，可以与 InDB 一致或有所删减
    pass
