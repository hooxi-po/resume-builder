# app/models/resume_models.py
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any # Ensure 'Any' is imported if used, though not explicitly in this version
from datetime import datetime, timezone # Import timezone for UTC awareness
import uuid # Ensure uuid is imported for generating default IDs

# --- 子模块的模型 ---
class PersonalInfo(BaseModel):
    name: Optional[str] = Field(None, example="张三")
    avatar: Optional[HttpUrl] = Field(None, example="https://example.com/avatar.jpg")
    title: Optional[str] = Field(None, example="软件工程师")
    email: Optional[str] = Field(None, example="zhangsan@example.com")
    phone: Optional[str] = Field(None, example="13800138000")
    linkedin: Optional[HttpUrl] = Field(None, example="https://linkedin.com/in/zhangsan")
    github: Optional[HttpUrl] = Field(None, example="https://github.com/zhangsan")
    website: Optional[HttpUrl] = Field(None, example="https://zhangsan.com")
    address: Optional[str] = Field(None, example="XX区XX路XX号")
    city: Optional[str] = Field(None, example="上海")
    country: Optional[str] = Field(None, example="中国")

    class Config:
        from_attributes = True # For Pydantic V2

class ExperienceItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    company: Optional[str] = Field(None, example="XX科技有限公司")
    role: Optional[str] = Field(None, example="前端开发工程师")
    location: Optional[str] = Field(None, example="上海市")
    startDate: Optional[str] = Field(None, example="2020-01")
    endDate: Optional[str] = Field(None, example="2022-12 或 至今")
    responsibilities: List[str] = Field(default_factory=list, example=["负责XX模块的开发与维护"]) # Changed to non-optional with default
    achievements: List[str] = Field(default_factory=list, example=["优化XX流程，效率提升20%"]) # Changed to non-optional with default

    class Config:
        from_attributes = True

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

    class Config:
        from_attributes = True

class ProjectItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: Optional[str] = Field(None, example="个人博客系统")
    description: Optional[str] = Field(None, example="基于Vue和FastAPI的个人博客")
    technologies: List[str] = Field(default_factory=list, example=["Vue.js", "FastAPI", "MongoDB"]) # Changed to non-optional
    url: Optional[HttpUrl] = Field(None, example="https://myblog.com")
    repoUrl: Optional[HttpUrl] = Field(None, example="https://github.com/user/myblog")
    startDate: Optional[str] = Field(None, example="2023-01")
    endDate: Optional[str] = Field(None, example="2023-05")

    class Config:
        from_attributes = True

class Skills(BaseModel):
    technical: List[str] = Field(default_factory=list, example=["JavaScript", "Python", "Vue.js"]) # Changed to non-optional
    languages: List[str] = Field(default_factory=list, example=["英语 (流利)", "中文 (母语)"]) # Changed to non-optional
    soft: List[str] = Field(default_factory=list, example=["团队合作", "沟通能力"]) # Changed to non-optional

    class Config:
        from_attributes = True

class CertificateItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: Optional[str] = Field(None, example="AWS解决方案架构师认证")
    issuingOrganization: Optional[str] = Field(None, example="Amazon Web Services")
    issueDate: Optional[str] = Field(None, example="2022-08")
    expirationDate: Optional[str] = Field(None, example="2025-08") # Optional
    credentialId: Optional[str] = Field(None, example="AWS123456XYZ")
    credentialUrl: Optional[HttpUrl] = Field(None, example="https://aw.cert/validate/123")

    class Config:
        from_attributes = True

class CustomSectionItemDetail(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    heading: Optional[str] = Field(None, example="XX编程竞赛一等奖")
    subheading: Optional[str] = Field(None, example="2019年全国大学生程序设计竞赛")
    description: Optional[str] = Field(None, example="团队负责人，主要负责算法设计与实现。")

    class Config:
        from_attributes = True

class CustomSectionItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: Optional[str] = Field(None, example="获奖经历")
    items: List[CustomSectionItemDetail] = Field(default_factory=list) # Changed to non-optional

    class Config:
        from_attributes = True

class ResumeMeta(BaseModel):
    template: str = Field("BasicTemplate", example="ModernTemplate") # Changed to non-optional
    accentColor: str = Field("#007bff", example="#FF5733") # Changed to non-optional
    fontFamily: str = Field("Arial, sans-serif", example="Roboto, sans-serif") # Changed to non-optional

    class Config:
        from_attributes = True

# --- 简历主模型 ---
class ResumeData(BaseModel):
    personalInfo: PersonalInfo = Field(default_factory=PersonalInfo)
    summary: Optional[str] = Field(None, example="一位经验丰富的软件工程师...")
    experience: List[ExperienceItem] = Field(default_factory=list)
    education: List[EducationItem] = Field(default_factory=list)
    projects: List[ProjectItem] = Field(default_factory=list)
    skills: Skills = Field(default_factory=Skills)
    certificates: List[CertificateItem] = Field(default_factory=list)
    customSections: List[CustomSectionItem] = Field(default_factory=list)
    meta: ResumeMeta = Field(default_factory=ResumeMeta)

    class Config:
        from_attributes = True

class ResumeBase(BaseModel):
    resume_name: str = Field(..., min_length=1, example="我的第一份技术简历") # Added min_length
    resume_data: ResumeData = Field(default_factory=ResumeData)

    class Config:
        from_attributes = True

class ResumeCreate(ResumeBase):
    pass # Inherits fields and config from ResumeBase

class ResumeUpdate(BaseModel): # Allows partial updates
    resume_name: Optional[str] = Field(None, min_length=1)
    resume_data: Optional[ResumeData] = None

    class Config:
        from_attributes = True

class ResumeInDB(ResumeBase):
    # id is aliased to _id for MongoDB, with a default UUID factory
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    user_id: str = Field(...) # This must be provided when creating an instance
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        populate_by_name = True # Allows use of alias '_id' when creating from dict
        from_attributes = True  # For Pydantic V2 (was orm_mode in V1)

class Resume(ResumeInDB):
    # This is the model that will be returned to the client.
    # It can be the same as ResumeInDB or have fewer fields.
    pass
