# app/routers/resume_router.py
from fastapi import APIRouter, Depends, HTTPException, status, Body
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

from app.models import resume_models, user_models
from app.core import security
from app.db.mongodb_utils import get_database
from bson import ObjectId # 用于处理MongoDB的ObjectId，如果需要的话，但我们用UUID字符串作为ID

router = APIRouter()

# --- 简历数据库操作辅助函数 ---
async def create_db_resume(db: AsyncIOMotorDatabase, resume_in: resume_models.ResumeCreate, user_id: str) -> resume_models.ResumeInDB:
    now = datetime.utcnow()
    # Pydantic V2
    # resume_data_dict = resume_in.resume_data.model_dump()
    # Pydantic V1
    resume_data_dict = resume_in.resume_data.dict()

    resume_db_obj = resume_models.ResumeInDB(
        resume_name=resume_in.resume_name,
        resume_data=resume_data_dict, # 存储完整的 resume_data 对象
        user_id=user_id,
        created_at=now,
        updated_at=now
    )
    # Pydantic V2
    # resume_db_dict = resume_db_obj.model_dump(by_alias=True) # by_alias=True 确保 _id
    # Pydantic V1
    resume_db_dict = resume_db_obj.dict(by_alias=True)

    result = await db["resumes"].insert_one(resume_db_dict)
    created_resume = await db["resumes"].find_one({"_id": result.inserted_id})
    if created_resume:
        return resume_models.ResumeInDB(**created_resume)
    raise HTTPException(status_code=500, detail="无法创建简历。")

async def get_db_resume_by_id(db: AsyncIOMotorDatabase, resume_id: str, user_id: str) -> Optional[resume_models.ResumeInDB]:
    resume_dict = await db["resumes"].find_one({"_id": resume_id, "user_id": user_id})
    if resume_dict:
        return resume_models.ResumeInDB(**resume_dict)
    return None

async def get_db_resumes_by_user_id(db: AsyncIOMotorDatabase, user_id: str) -> List[resume_models.ResumeInDB]:
    resumes = []
    cursor = db["resumes"].find({"user_id": user_id})
    async for resume_dict in cursor:
        resumes.append(resume_models.ResumeInDB(**resume_dict))
    return resumes

async def update_db_resume(db: AsyncIOMotorDatabase, resume_id: str, resume_update: resume_models.ResumeUpdate, user_id: str) -> Optional[resume_models.ResumeInDB]:
    existing_resume = await get_db_resume_by_id(db, resume_id, user_id)
    if not existing_resume:
        return None

    update_data = {}
    if resume_update.resume_name is not None:
        update_data["resume_name"] = resume_update.resume_name
    if resume_update.resume_data is not None:
        # Pydantic V2
        # update_data["resume_data"] = resume_update.resume_data.model_dump()
        # Pydantic V1
        update_data["resume_data"] = resume_update.resume_data.dict()
    
    if not update_data: # 如果没有提供任何更新数据
        return existing_resume # 或者抛出错误，取决于业务逻辑

    update_data["updated_at"] = datetime.utcnow()

    result = await db["resumes"].update_one(
        {"_id": resume_id, "user_id": user_id},
        {"$set": update_data}
    )
    if result.modified_count == 1:
        updated_resume = await get_db_resume_by_id(db, resume_id, user_id)
        return updated_resume
    # 如果没有修改（例如，提供的数据与现有数据相同），或者更新失败
    return existing_resume # 或者返回None/抛出错误


async def delete_db_resume(db: AsyncIOMotorDatabase, resume_id: str, user_id: str) -> bool:
    result = await db["resumes"].delete_one({"_id": resume_id, "user_id": user_id})
    return result.deleted_count > 0


# --- API 端点 ---
@router.post("/", response_model=resume_models.Resume, status_code=status.HTTP_201_CREATED)
async def create_resume(
    resume_in: resume_models.ResumeCreate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: user_models.User = Depends(security.get_current_active_user)
):
    """
    为当前认证用户创建一份新简历。
    """
    created_resume = await create_db_resume(db, resume_in, user_id=str(current_user.id))
    return created_resume

@router.get("/", response_model=List[resume_models.Resume])
async def read_resumes(
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: user_models.User = Depends(security.get_current_active_user),
    skip: int = 0, # 用于分页
    limit: int = 100 # 用于分页
):
    """
    获取当前认证用户的所有简历。
    """
    # 注意：这里的分页逻辑直接在 find() 中实现会更高效
    # cursor = db["resumes"].find({"user_id": str(current_user.id)}).skip(skip).limit(limit)
    # resumes = []
    # async for resume_dict in cursor:
    #     resumes.append(resume_models.Resume(**resume_dict))
    # return resumes
    resumes = await get_db_resumes_by_user_id(db, user_id=str(current_user.id))
    # 手动分页 (如果上面直接用 skip/limit, 则不需要这部分)
    return resumes[skip : skip + limit]


@router.get("/{resume_id}", response_model=resume_models.Resume)
async def read_resume(
    resume_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: user_models.User = Depends(security.get_current_active_user)
):
    """
    获取指定ID的简历。用户只能访问自己的简历。
    """
    resume = await get_db_resume_by_id(db, resume_id, user_id=str(current_user.id))
    if resume is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未找到简历或无权访问")
    return resume

@router.put("/{resume_id}", response_model=resume_models.Resume)
async def update_resume(
    resume_id: str,
    resume_update: resume_models.ResumeUpdate, # 请求体
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: user_models.User = Depends(security.get_current_active_user)
):
    """
    更新指定ID的简历。用户只能更新自己的简历。
    """
    updated_resume = await update_db_resume(db, resume_id, resume_update, user_id=str(current_user.id))
    if updated_resume is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未找到简历或更新失败")
    return updated_resume

@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: user_models.User = Depends(security.get_current_active_user)
):
    """
    删除指定ID的简历。用户只能删除自己的简历。
    """
    deleted = await delete_db_resume(db, resume_id, user_id=str(current_user.id))
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未找到要删除的简历")
    return # 返回 204 No Content
