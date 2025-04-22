from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# 🔗 中間テーブル：Task と Tag の多対多リンク
class TagLink(SQLModel, table=True):
    task_id: Optional[int] = Field(default=None, foreign_key="task.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)

# 🗂 タスクテーブル
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    is_done: bool = False
    due_date: Optional[datetime] = None  # ← ★ 追加：期限（任意）
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    tags: List["Tag"] = Relationship(back_populates="tasks", link_model=TagLink)

# 🏷 タグテーブル
class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    tasks: List[Task] = Relationship(back_populates="tags", link_model=TagLink)
    
# 📦 TaskCreate にも due_date を追加
class TaskCreate(BaseModel):
    title: str
    is_done: bool = False
    due_date: Optional[datetime] = None  # ← ★追加
    tags: Optional[List[str]] = []

from pydantic import BaseModel
from typing import Optional, List

# 省略：TagLink, Task, Tagなどはここに定義済みと仮定

# ✅ TaskUpdate にも due_date を追加
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    is_done: Optional[bool] = None
    due_date: Optional[datetime] = None  # ← ★追加
    tags: Optional[List[str]] = []

    class Config:
        from_attributes = True
        
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str