from pydantic import BaseModel
from typing import Optional, List

class Message(BaseModel):
    message: str
    
# response_models.py の上部に追加！
class TagRead(BaseModel):
    id: int
    name: str

class TaskRead(BaseModel):
    id: int
    title: str
    is_done: bool
    tags: List[TagRead] = []  # ← タグも含めて返す

    class Config:
        orm_mode = True