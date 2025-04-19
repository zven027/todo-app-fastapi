from sqlmodel import Session, select
from pydantic import BaseModel
from typing import List
from models import Task
from database import engine
from sqlmodel import select
from models import TaskUpdate
from fastapi import HTTPException
from datetime import datetime
from typing import Optional
from sqlalchemy import or_
from models import TaskCreate
from models import Tag
from sqlalchemy.orm import selectinload


def get_tasks() -> List[Task]:
    with Session(engine) as session:
        statement = select(Task)
        results= session.exec(statement)
        return results.all()

def get_task_or_404(task_id: int, session: Session) -> Task:
    task = session.exec(
        select(Task)
        .where(Task.id == task_id)
        .options(selectinload(Task.tags))  # 👈 タグを事前に読み込む！
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
def create_task(task: Task) -> Task:
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)  # 更新 ID 等自动生成字段
        return task

def delete_task(task_id: int) -> bool:
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if task:
            session.delete(task)
            session.commit()
            return True
        return False
    
def mark_task_done(task_id: int) -> bool:
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if task:
            task.is_done = True
            session.add(task)
            session.commit()
            return True
        return False


def update_task_with_tags(task_id: int, task_data: TaskUpdate, session: Session) -> Task:
    task = get_task_or_404(task_id, session)

    task.title = task_data.title
    task.is_done = task_data.is_done
    task.updated_at = datetime.utcnow()

    # タグの更新
    if task_data.tags is not None:
        tag_objects = []
        for tag_name in task_data.tags:
            tag = session.exec(select(Tag).where(Tag.name == tag_name)).first()
            if not tag:
                tag = Tag(name=tag_name)
                session.add(tag)
                session.flush()
            tag_objects.append(tag)
        task.tags = tag_objects  # ← 多対多の更新

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def filter_tasks(is_done: bool, title: Optional[str], session: Session) -> List[Task]:
    statement = select(Task).where(Task.is_done == is_done)
    if title:
        statement = statement.where(Task.title.contains(title))  # タイトルに含まれるかを検索
    results = session.exec(statement).all()
    return results


def delete_task_or_404(task_id: int):
    success = delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="指定 ID のタスクが存在しません")
    
def advanced_search_tasks(session: Session, is_done: Optional[bool], title: Optional[str]) -> List[Task]:
    statement = select(Task)

    if is_done is not None:
        statement = statement.where(Task.is_done == is_done)

    if title:
        statement = statement.where(Task.title.contains(title))

    results = session.exec(statement).all()
    return results

def get_tasks_paginated(offset: int, limit: int, session: Session) -> List[Task]:
    statement = (
        select(Task)
        .order_by(Task.created_at.desc())  # 作成日時の降順に並び替え
        .offset(offset)
        .limit(limit)
    )
    return session.exec(statement).all()

def get_task(task_id: int) -> Optional[Task]:
    with Session(engine) as session:
        return session.get(Task, task_id)

def create_task_with_tags(task_data: TaskCreate, session: Session) -> Task:
    # タスクを作成（TagLinkはまだ付けない）
    task = Task(title=task_data.title, is_done=task_data.is_done)

    for tag_name in task_data.tags:
        # タグがすでに存在するかを確認
        tag = session.exec(select(Tag).where(Tag.name == tag_name)).first()
        if not tag:
            tag = Tag(name=tag_name)
            session.add(tag)
            session.flush()  # IDを得るために必要
        # タスクにタグを紐づけ
        task.tags.append(tag)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def get_all_tags(session: Session) -> List[Tag]:
    return session.exec(select(Tag)).all()

# 特定のタグ名に紐づくタスクを取得
def get_tasks_by_tag(tag_name: str, session: Session) -> List[Task]:
    statement = select(Task).join(Task.tags).where(Tag.name == tag_name)
    return session.exec(statement).all()

def search_tasks(is_done: bool, session: Session) -> List[Task]:
    statement = select(Task).where(Task.is_done == is_done).order_by(Task.created_at.desc())
    tasks = session.exec(statement).all()
    return tasks