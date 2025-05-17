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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login/access-token") # 与登录路由匹配

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
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_user_by_username_for_auth(db: AsyncIOMotorDatabase, username: str) -> Optional[user_models.UserInDB]:
    """
    Helper function to get user from DB for authentication purposes.
    Moved from auth_router to be used by get_current_user.
    """
    user_dict = await db["users"].find_one({"username": username})
    if user_dict:
        return user_models.UserInDB(**user_dict)
    return None

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> user_models.UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        user_id: Optional[str] = payload.get("user_id") # 获取 user_id
        if username is None or user_id is None:
            raise credentials_exception
        token_data = user_models.TokenData(username=username, user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    user = await get_user_by_username_for_auth(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    # 确保从token中获取的user_id与数据库中的用户id匹配 (可选的额外安全检查)
    if str(user.id) != token_data.user_id:
        raise credentials_exception
        
    return user

async def get_current_active_user(
    current_user: user_models.UserInDB = Depends(get_current_user)
) -> user_models.UserInDB:
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已被禁用")
    return current_user
