# app/models/user_models.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict # 导入 ConfigDict
from typing import Optional
import uuid
from datetime import datetime, timezone # 确保导入 timezone

class UserBase(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    username: str = Field(..., min_length=3, max_length=50, example="john_doe")
    # full_name: Optional[str] = Field(None, example="John Doe") # 可选字段

    # Pydantic V2: 为基础模型添加 model_config (如果需要，例如为了 from_attributes)
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, example="strongpassword123")

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    # full_name: Optional[str] = None
    # password: Optional[str] = Field(None, min_length=6) # 如果允许更新密码

    # Pydantic V2: 为更新模型添加 model_config
    # extra='ignore' 可以防止未在模型中定义的字段在更新时导致错误
    model_config = ConfigDict(from_attributes=True, extra='ignore')

class UserInDBBase(UserBase):
    # 假设用户 ID 也使用字符串形式的 UUID，与 resume_models.py 保持一致
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    hashed_password: str
    # Pydantic V2 中，如果字段不是 Optional，最好有明确的默认值
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    # disabled: Optional[bool] = False # 'is_active' 更常用, 如果使用 'disabled', 确保有默认值
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Pydantic V2 配置
    model_config = ConfigDict(
        populate_by_name=True, # 允许按字段名或别名填充
        from_attributes=True   # 替换 V1 中的 orm_mode = True
    )

class User(UserInDBBase):
    # 返回给客户端的模型
    # 默认继承 UserInDBBase 的所有字段。
    # 如果需要排除敏感字段（如 hashed_password），可以覆盖 model_config:
    # model_config = ConfigDict(
    #     # populate_by_name=True, # 已继承
    #     # from_attributes=True,  # 已继承
    #     fields={'hashed_password': {'exclude': True}} # 示例：排除 hashed_password
    # )
    pass


class UserInDB(UserInDBBase):
    # 代表存储在数据库中的完整用户对象
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[str] = None # 在 token 中存储用户 ID 会很方便
