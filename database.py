from sqlmodel import SQLModel, create_engine

# 连接到本地 SQLite 数据库文件（如果没有会自动创建）
sqlite_url="sqlite:///./tasks.db"
engine = create_engine(sqlite_url,echo=True)

# 自动根据模型创建数据库中的表
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)