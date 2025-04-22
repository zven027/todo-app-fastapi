from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
import os
from dotenv import load_dotenv
# .env ファイルを読み込む
load_dotenv()

# DATABASE_URL を環境変数から取得
DATABASE_URL = os.getenv("DATABASE_URL")

# PostgreSQL 用のエンジンを作成
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)
    
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

print("DATABASE_URL:", DATABASE_URL)