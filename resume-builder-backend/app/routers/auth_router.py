# app/routers/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Optional, List, Any 
from app.models import user_models
from app.core import security # 我们将在这里创建 security.py
from app.core.config import settings
from app.db.mongodb_utils import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()

# --- 辅助函数 (通常会放在 app.core.security 或 app.services.user_service) ---
async def get_user_by_email(db: AsyncIOMotorDatabase, email: str) -> Optional[user_models.UserInDB]:
    user_dict = await db["users"].find_one({"email": email})
    if user_dict:
        return user_models.UserInDB(**user_dict)
    return None

async def get_user_by_username(db: AsyncIOMotorDatabase, username: str) -> Optional[user_models.UserInDB]:
    user_dict = await db["users"].find_one({"username": username})
    if user_dict:
        return user_models.UserInDB(**user_dict)
    return None

async def create_db_user(db: AsyncIOMotorDatabase, user_in: user_models.UserCreate) -> user_models.UserInDB:
    hashed_password = security.get_password_hash(user_in.password)
    
    # Pydantic V2: 使用 model_dump()
    user_db_data = user_in.model_dump(exclude={"password"})

    # UserInDBBase 已经包含了 is_active 和 is_superuser 的默认值
    user_db_obj = user_models.UserInDBBase(**user_db_data, hashed_password=hashed_password)
    
    # Pydantic V2: 使用 model_dump()
    # by_alias=True 确保 _id 被正确用于 MongoDB 插入
    user_db_dict_for_insertion = user_db_obj.model_dump(by_alias=True)

    result = await db["users"].insert_one(user_db_dict_for_insertion)
    created_user_from_db = await db["users"].find_one({"_id": result.inserted_id})
    
    if created_user_from_db:
        return user_models.UserInDB(**created_user_from_db)
    raise HTTPException(status_code=500, detail="无法创建用户。") # "Could not create user."


@router.post("/register", response_model=user_models.User, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: user_models.UserCreate,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    """
    注册新用户。
    - **email**: 用户的邮箱地址 (必须唯一)。
    - **username**: 用户名 (必须唯一)。
    - **password**: 用户密码。
    """
    existing_user_email = await get_user_by_email(db, user_in.email)
    if existing_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册。", # "Email already registered."
        )
    existing_user_username = await get_user_by_username(db, user_in.username)
    if existing_user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该用户名已被使用。", # "Username already taken."
        )
    
    created_user = await create_db_user(db, user_in)
    return created_user


@router.post("/login/access-token", response_model=user_models.Token)
async def login_for_access_token(
    db: AsyncIOMotorDatabase = Depends(get_database),
    form_data: OAuth2PasswordRequestForm = Depends() # email作为username字段
):
    """
    用户登录以获取访问令牌。
    使用 OAuth2PasswordRequestForm, 表单字段为 `username` (这里用作邮箱) 和 `password`。
    """
    # 注意：FastAPI 的 OAuth2PasswordRequestForm 期望字段名为 'username'。
    # 如果你的前端发送的是 'email'，你需要确保前端表单字段名是 'username'，
    # 或者在后端自定义 OAuth2PasswordRequestForm 以接受 'email'。
    # 当前代码假设前端发送的 'username' 字段实际上是用户的邮箱。
    user = await get_user_by_email(db, form_data.username) # form_data.username 将是用户输入的邮箱
    
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误", # "Incorrect email or password"
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 这一步是正确的，与 security.py 中的 get_current_active_user 保持一致
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已被禁用") # "Inactive user"

    access_token_expires = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = security.create_access_token(
        data={"sub": user.username, "user_id": str(user.id)}, # 使用 username 作为 subject, 并包含 user_id
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=user_models.User)
async def read_users_me(
    current_user: user_models.User = Depends(security.get_current_active_user) # 依赖注入当前用户
):
    """
    获取当前已认证用户的信息。
    """
    return current_user
