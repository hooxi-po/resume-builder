# app/db/mongodb_utils.py
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings # 确保 app.core.config.py 文件存在且配置正确

class DataBase:
    client: AsyncIOMotorClient = None # MongoDB 客户端实例
    db: AsyncIOMotorDatabase = None   # MongoDB 数据库实例

db_manager = DataBase() # 创建一个全局的数据库管理器实例

async def connect_to_mongo():
    """
    异步连接到 MongoDB 数据库。
    此函数应在应用启动时调用。
    """
    print("尝试连接到 MongoDB...")
    try:
        # 从配置中获取 MongoDB 连接 URL
        db_manager.client = AsyncIOMotorClient(settings.MONGODB_URL)
        # 从配置中获取数据库名称
        db_manager.db = db_manager.client[settings.DATABASE_NAME]
        
        # 发送一个 ping 命令来验证连接是否成功
        await db_manager.client.admin.command('ping')
        print(f"成功连接到 MongoDB! 数据库: {settings.DATABASE_NAME}")
    except Exception as e:
        print(f"连接 MongoDB 失败: {e}")
        # 在实际应用中，如果数据库连接对应用至关重要，
        # 您可能需要在这里抛出异常或执行其他错误处理逻辑，
        # 例如，如果无法连接，则阻止应用启动。
        # raise RuntimeError(f"无法连接到 MongoDB: {e}") from e

async def close_mongo_connection():
    """
    异步关闭 MongoDB 连接。
    此函数应在应用关闭时调用。
    """
    print("尝试关闭 MongoDB 连接...")
    if db_manager.client:
        db_manager.client.close()
        print("MongoDB 连接已关闭。")

def get_database() -> AsyncIOMotorDatabase:
    """
    获取数据库实例。

    Raises:
        RuntimeError: 如果数据库未初始化 (即 connect_to_mongo 未被成功调用)。

    Returns:
        AsyncIOMotorDatabase: 当前的数据库实例。
    """
    if db_manager.db is None:
        # 这种错误理论上不应该在正常的请求处理流程中发生，
        # 因为 connect_to_mongo() 应该已经在应用启动时被调用。
        raise RuntimeError("数据库未初始化。请确保 connect_to_mongo 已被成功调用。")
    return db_manager.db
