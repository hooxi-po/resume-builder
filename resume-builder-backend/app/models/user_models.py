# app/models/user_models.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import uuid # 用于生成唯一的ID

class UserBase(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    username: str = Field(..., min_length=3, max_length=50, example="john_doe")
    # full_name: Optional[str] = Field(None, example="John Doe") # 可选字段

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, example="strongpassword123")

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    # full_name: Optional[str] = None
    # password: Optional[str] = Field(None, min_length=6) # 如果允许更新密码

class UserInDBBase(UserBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id") # MongoDB 使用 _id
    hashed_password: str
    disabled: Optional[bool] = False

    class Config:
        populate_by_name = True # 允许使用 alias (_id) 进行填充
        # Pydantic V2:
        # from_attributes = True # 允许从 ORM 对象（或类似对象）创建模型
        # Pydantic V1:
        orm_mode = True # 允许从 ORM 对象（或类似对象）创建模型

class User(UserInDBBase):
    # 可以在这里添加更多返回给客户端的字段 (不包括敏感信息)
    pass

class UserInDB(UserInDBBase):
    # 数据库中存储的完整用户模型
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[str] = None # 将用户ID也存储在token中会很方便
