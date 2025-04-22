from fastapi import FastAPI, HTTPException
from fastapi import HTTPException, Path
from typing import List
from typing import Optional
from models import Task
from models import  TaskUpdate
from database import create_db_and_tables
from fastapi import Query
from database import engine  # 你自己的 engine
import crud
from response_models import Message  # 新しく追加
from fastapi import status
import logging
from models import TaskCreate, TaskUpdate
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from sqlmodel import Session
from models import Tag
from response_models import TaskRead, TagRead, Message
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles  # CSS使いたいとき用
from fastapi import Query
from typing import Optional
from datetime import datetime
from sqlmodel import select
from sqlmodel import SQLModel, Field
from auth import hash_password
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from database import engine
from models import User
from auth import verify_password
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from models import User
from auth import hash_password
from database import engine
from auth import verify_password, create_access_token  # 👈 トークン関数
from auth import get_current_user
from fastapi import FastAPI
from auth import login_token  # auth.pyからインポート
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

app=FastAPI()

templates = Jinja2Templates(directory="templates")
templates.env.globals["now"] = datetime.now  # 👈 これを追加



# 程序启动时自动建表（防止漏建）
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
@app.on_event("startup")
def on_startup():
    from auth import SECRET_KEY  # ← auth.py から読み込んだ SECRET_KEY
    print(f"[DEBUG] SECRET_KEY: {SECRET_KEY}")  # 👈 追加！
    create_db_and_tables()
    
@app.post("/login")
def login(email: str, password: str):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        
        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect password")

        # 👇 トークンを作成
        access_token = create_access_token(data={"sub": str(user.id)})

        return {
            "message": "Login successful",
            "user_id": user.id,
            "access_token": access_token,
            "token_type": "bearer"
        }
    
@app.post("/register")
def register_user(email: str, password: str):
    with Session(engine) as session:
        # すでに同じ email があるか確認
        existing_user = session.exec(
            select(User).where(User.email == email)
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # 新しいユーザーを作成（パスワードをハッシュ化）
        user = User(email=email, hashed_password=hash_password(password))
        session.add(user)
        session.commit()
        session.refresh(user)

        return {"message": "User registered", "user_id": user.id}


@app.get("/me")
def get_me(user: User = Depends(get_current_user)):
    return {"user_id": user.id, "email": user.email}

@app.get(
    "/tasks",
    response_model=List[Task],
    summary="タスクをページ単位で取得",
    description="作成日時の降順で取得。offset（開始位置）とlimit（最大件数）を指定可能。"
)
def read_tasks(offset: int = 0, limit: int = 10):
    with Session(engine) as session:
        return crud.get_tasks_paginated(offset, limit, session)


@app.get(
    "/tasks/search",
    response_model=List[Task],
    summary="完了状態とタイトルでタスクをフィルター",
    description="完了状態（is_done）とタイトルキーワード（title）でタスクを検索します。"
)
def filter_tasks_endpoint(
    is_done: bool = Query(..., description="完了済みタスク: true, 未完了タスク: false"),
    title: Optional[str] = Query(None, description="タイトルに含まれるキーワード")
):
    with Session(engine) as session:
        tasks = crud.filter_tasks(is_done=is_done, title=title, session=session)
        return tasks

def filter_tasks_by_done(
    is_done: bool = Query(..., description="完了済みタスク: true, 未完了タスク: false")
):
    """
    クエリパラメータ `is_done` に応じてタスクをフィルターするAPI。

    Parameters:
    - is_done (bool): 完了状態でフィルター。true=完了、false=未完了。

    Returns:
    - List[Task]: フィルターされたタスク一覧。
    """
    with Session(engine) as session:
        tasks = crud.search_tasks(is_done, session)
        return tasks


@app.get("/tasks/by_tag", response_model=List[Task], summary="タグでタスクを検索")
def read_tasks_by_tag(tag: str = Query(..., description="検索対象のタグ名")):
    with Session(engine) as session:
        return crud.get_tasks_by_tag(tag, session)

@app.get("/tasks/{task_id}", response_model=TaskRead, summary="指定IDのタスクを取得", description="タスクIDで1件のタスクを取得します。")
def read_task(task_id: int):
    with Session(engine) as session:
        return crud.get_task_or_404(task_id, session)


@app.post("/toggle_done/{task_id}")
def toggle_task_done(task_id: int):
    with Session(engine) as session:
        task = crud.get_task_or_404(task_id, session)
        task.is_done = not task.is_done
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
    return RedirectResponse(url="/", status_code=303)

# UIルート：フォームから追加
@app.post("/add")
def add_task(title: str = Form(...), due_date: Optional[str] = Form(None)):
    with Session(engine) as session:
        # 期限が入力されていたら文字列を datetime に変換
        due = datetime.strptime(due_date, "%Y-%m-%d") if due_date else None

        # 期限付きタスクを作成
        new_task = Task(title=title, due_date=due)
        session.add(new_task)
        session.commit()
    return RedirectResponse(url="/", status_code=303)

@app.put("/tasks/{task_id}", response_model=Task, summary="タスクを更新", description="タスクの内容や完了状況を変更します")
def update_task(task_id: int, task_update: TaskUpdate):
    # 空タイトルのバリデーション（空文字や空白のみ）
    if task_update.title is not None and not task_update.title.strip():
        raise HTTPException(status_code=400, detail="タスクのタイトルは空にできません")

    with Session(engine) as session:
        task = crud.update_task_with_tags(task_id, task_update, session)
        if not task:
            raise HTTPException(status_code=404, detail="指定されたIDのタスクは存在しません")
            return crud.update_task_with_tags(task_id, task_update, session)
    
# PATCH メソッドで完了フラグを変更する（部分更新）
@app.patch("/tasks/{task_id}/done", summary="タスクを完了にする", description="指定したIDのタスクの is_done を True に更新します")
def mark_done(task_id: int):
    success = crud.mark_task_done(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="指定IDのタスクが見つかりません")
    return {"message": "タスクを完了しました"}

# main.py 内
from fastapi import status

logger = logging.getLogger("uvicorn")

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="タスクの削除")
def delete_task(task_id: int):
    logger.info(f"タスク削除リクエスト受信: task_id={task_id}")
    success = crud.delete_task(task_id)
    if not success:
        logger.warning(f"削除失敗: task_id={task_id}")
        raise HTTPException(status_code=404, detail="指定されたタスクが見つかりません")
    logger.info(f"タスク削除成功: task_id={task_id}")



@app.get("/tags", response_model=List[Tag], summary="全タグ一覧", description="登録されている全てのタグを取得します")
def read_tags():
    with Session(engine) as session:
        return crud.get_all_tags(session)


@app.post("/delete/{task_id}")
def delete_task(task_id: int):
    with Session(engine) as session:
        task = crud.get_task_or_404(task_id, session)
        session.delete(task)
        session.commit()
    return RedirectResponse(url="/", status_code=303)

@app.post("/add_tag/{task_id}")
def add_tag(task_id: int, tag_name: str = Form(...)):
    with Session(engine) as session:
        task = crud.get_task_or_404(task_id, session)

        # 既存タグの確認・取得 or 作成
        tag = session.exec(select(Tag).where(Tag.name == tag_name)).first()
        if not tag:
            tag = Tag(name=tag_name)
            session.add(tag)
            session.flush()  # IDを確保

        # 中間テーブルでリンク（重複チェックもするなら別途）
        if tag not in task.tags:
            task.tags.append(tag)

        session.add(task)
        session.commit()

    return RedirectResponse(url="/", status_code=303)

@app.get("/filter_by_tag", response_class=HTMLResponse)
def filter_by_tag(request: Request, tag: str):
    with Session(engine) as session:
        tasks = crud.get_tasks_by_tag(tag, session)
        tags = crud.get_all_tags(session)
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "tasks": tasks,
                "tags": tags,
                "selected_tag": tag
            },
        )

@app.get("/", response_class=HTMLResponse)
def read_todo_page(request: Request, is_done: Optional[bool] = Query(None)):
    with Session(engine) as session:
        # 有フィルターならフィルター適用、なければ全件
        if is_done is None:
            tasks = crud.get_tasks_paginated(offset=0, limit=100, session=session)
        else:
            tasks = crud.search_tasks(is_done=is_done, session=session)

        tags = crud.get_all_tags(session)

        return templates.TemplateResponse("index.html", {
            "request": request,
            "tasks": tasks,
            "tags": tags,
            "is_done_filter": is_done,
        })
        

@app.get("/edit/{task_id}", response_class=HTMLResponse)
def edit_task_form(request: Request, task_id: int):
    with Session(engine) as session:
        task = crud.get_task_or_404(task_id, session)
        return templates.TemplateResponse("edit.html", {
            "request": request,
            "task": task
        })
        
@app.post("/edit/{task_id}")
def edit_task_submit(
    task_id: int,
    title: str = Form(...),
    is_done: str = Form(...),
    due_date: Optional[str] = Form(None)
):
    with Session(engine) as session:
        task = crud.get_task_or_404(task_id, session)

        task.title = title
        task.is_done = (is_done == "true")

        if due_date:
            task.due_date = datetime.strptime(due_date, "%Y-%m-%d")
        else:
            task.due_date = None

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()

    return RedirectResponse(url="/", status_code=303)

@app.post("/token")
def token_endpoint(form_data: OAuth2PasswordRequestForm = Depends()):
    return login_token(form_data)

import os
import uvicorn

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))  # ← Railway 自动注入 PORT
    uvicorn.run("main:app", host="0.0.0.0", port=port)