# app/core/security.py
from datetime import datetime, timedelta, timezone
from typing import Optional, Any

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.models import user_models # 确保路径正确
from app.db.mongodb_utils import get_database # 确保路径正确
from motor.motor_asyncio import AsyncIOMotorDatabase


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 确保 tokenUrl 与你的 auth_router.py 中登录端点的路径完全一致
# 如果 auth_router.py 中的登录路径是 /api/auth/login/access-token
# 这里的 tokenUrl 应该是 "auth/login/access-token" (相对于 /api 前缀)
# 或者 "/api/auth/login/access-token" (如果你的 API 客户端不自动加 /api 前缀)
# 从之前的日志看，前端请求的是 /api/auth/login/access-token，所以这里应该是这个完整路径或相对路径
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login/access-token")

ALGORITHM = settings.JWT_ALGORITHM
SECRET_KEY = settings.JWT_SECRET_KEY

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # 确保 settings.ACCESS_TOKEN_EXPIRE_MINUTES 是整数或浮点数
        expire = datetime.now(timezone.utc) + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_user_by_username_for_auth(db: AsyncIOMotorDatabase, username: str) -> Optional[user_models.UserInDB]:
    """
    辅助函数，用于身份验证目的从数据库获取用户。
    """
    user_dict = await db["users"].find_one({"username": username})
    if user_dict:
        # 确保 UserInDB 模型能正确处理从数据库来的 user_dict
        # 特别是 _id 到 id 的映射，以及 is_active 等字段
        return user_models.UserInDB(**user_dict)
    return None

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> user_models.UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据", # "Could not validate credentials"
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        user_id: Optional[str] = payload.get("user_id") # 获取 user_id
        
        if username is None: # user_id 也可以是 None，取决于你的 token 设计
            raise credentials_exception
        # TokenData 模型用于验证 payload 结构，如果 username 或 user_id 缺失，会在这里失败
        token_data = user_models.TokenData(username=username, user_id=user_id)

    except JWTError:
        raise credentials_exception
    except Exception as e: # 捕获 Pydantic 验证错误等
        print(f"Error decoding or validating token data: {e}")
        raise credentials_exception
    
    user = await get_user_by_username_for_auth(db, username=token_data.username)
    
    if user is None:
        raise credentials_exception
    
    # 可选的额外安全检查: 确保 token 中的 user_id 与从数据库中获取的 user.id 匹配
    # 确保 user.id 是字符串类型进行比较
    if token_data.user_id and str(user.id) != token_data.user_id:
        print(f"Token user_id ({token_data.user_id}) does not match DB user.id ({user.id})")
        raise credentials_exception
        
    return user

async def get_current_active_user(
    current_user: user_models.UserInDB = Depends(get_current_user)
) -> user_models.UserInDB:
    # 修改这里：检查 is_active 字段而不是 disabled
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已被禁用") # "Inactive user"
    return current_user
