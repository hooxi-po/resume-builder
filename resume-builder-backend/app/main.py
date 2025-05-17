# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.db.mongodb_utils import connect_to_mongo, close_mongo_connection
from app.routers import auth_router, resume_router # 引入路由
from app.core.config import settings # 确保settings被加载

# lifespan 事件处理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("应用启动...")
    await connect_to_mongo()
    yield
    print("应用关闭...")
    await close_mongo_connection()

app = FastAPI(
    title="简历生成器 API",
    description="用于简历生成器应用后端的API服务。",
    version="0.1.0",
    lifespan=lifespan
)

# 配置CORS
origins = [
    "http://localhost:5173",  # Vue开发服务器的默认端口 (Vite)
    "http://localhost:3000",  # React开发服务器常见端口
    "http://localhost:8080",  # Vue开发服务器的常见端口 (Vue CLI)
    # 如果您的前端在其他地址，也需要添加
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"欢迎来到简历生成器API! (FastAPI) DB: {settings.DATABASE_NAME}"}

# 注册路由
app.include_router(auth_router.router, prefix="/api/auth", tags=["身份认证"])
app.include_router(resume_router.router, prefix="/api/resumes", tags=["简历管理"])

# 用于测试数据库连接的临时端点 (可选)
# from app.db.mongodb_utils import get_database
# @app.get("/ping-db", tags=["Test"])
# async def ping_db_endpoint(): # 重命名以避免与内部函数冲突
#     db = get_database()
#     try:
#         await db.command('ping') # 使用 await 因为 get_database 返回的是 AsyncIOMotorDatabase
#         return {"status": "MongoDB is connected and reachable"}
#     except Exception as e:
#         return {"status": "MongoDB connection error", "error": str(e)}

