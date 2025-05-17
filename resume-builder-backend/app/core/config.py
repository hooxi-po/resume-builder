# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict # For Pydantic V2+
# from pydantic import BaseSettings # For Pydantic V1 if you are using it

import os
from dotenv import load_dotenv

# 构建 .env 文件的绝对路径
# 项目根目录是此文件 (config.py) 的上两级目录 (core -> app -> project_root)
# PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# DOTENV_PATH = os.path.join(PROJECT_ROOT, ".env")
# print(f"尝试加载 .env 文件从: {DOTENV_PATH}") # 调试路径

# load_dotenv(DOTENV_PATH) # 从指定路径加载 .env 文件
# 或者，如果 .env 文件与运行 uvicorn 的目录相同 (通常是项目根目录)，
# pydantic-settings 会自动查找，或者 load_dotenv() 不带参数也能工作。
load_dotenv() # 尝试从当前工作目录或其父目录加载 .env

class Settings(BaseSettings):
    """
    应用配置类。
    这些设置将从环境变量或 .env 文件中加载。
    """
    # MongoDB 配置
    MONGODB_URL: str = "mongodb://localhost:27017" # 默认值，如果 .env 中未设置
    DATABASE_NAME: str = "resume_builder_db"   # 默认值

    # JWT (JSON Web Token) 配置
    JWT_SECRET_KEY: str = "your_default_secret_key_please_change_in_env" # 默认值，强烈建议在 .env 中覆盖
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # 访问令牌的有效期（分钟）

    # Pydantic V2+ syntax for loading from .env file and other settings
    model_config = SettingsConfigDict(
        env_file=".env",      # 指定 .env 文件名
        env_file_encoding='utf-8', # 指定 .env 文件编码
        extra='ignore'        # 忽略 .env 文件中多余的变量
    )

    # Pydantic V1 syntax for loading from .env file
    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = 'utf-8'
    #     extra = "ignore"

# 创建一个全局的配置实例，应用的其他部分可以导入和使用它
settings = Settings()

# 打印加载的设置 (用于调试，生产环境中可以移除)
# print("--- 应用配置已加载 ---")
# print(f"MONGODB_URL: {settings.MONGODB_URL}")
# print(f"DATABASE_NAME: {settings.DATABASE_NAME}")
# print(f"JWT_SECRET_KEY (部分显示): {settings.JWT_SECRET_KEY[:5]}...") # 不要完整打印密钥
# print(f"JWT_ALGORITHM: {settings.JWT_ALGORITHM}")
# print(f"ACCESS_TOKEN_EXPIRE_MINUTES: {settings.ACCESS_TOKEN_EXPIRE_MINUTES}")
# print("-------------------------")

