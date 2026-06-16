from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User, Task, Tag
from schemas import (
    UserCreate,
    UserResponse,
    TaskCreate,
    TaskResponse,
    TagCreate,
    TagResponse
)
app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Creating user using id
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        name=user.name,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Task adding for specific user
@app.post("/users/{user_id}/tasks", response_model=TaskResponse)
def add_task(
        user_id: int,
        task: TaskCreate,
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    new_task = Task(
        title=task.title,
        user_id=user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

#Displaying all tasks of a user
@app.get("/users/{user_id}/tasks",
         response_model=list[TaskResponse])
def get_tasks(
        user_id: int,
        db: Session = Depends(get_db)
):
    tasks = db.query(Task).filter(
        Task.user_id == user_id
    ).all()
    return tasks

@app.get("/users/{user_id}/pending",
         response_model=list[TaskResponse])
def get_pending_tasks(
        user_id: int,
        db: Session = Depends(get_db)
):
    tasks = db.query(Task).filter(
        Task.user_id == user_id,
        Task.completed == False
    ).all()
    return tasks

#Change tag to completed
@app.put("/tasks/{task_id}",
         response_model=TaskResponse)
def complete_task(
        task_id: int,
        db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    task.completed = True
    db.commit()
    db.refresh(task)
    return task

#Removing a task
@app.delete("/tasks/{task_id}")
def delete_task(
        task_id: int,
        db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    db.delete(task)
    db.commit()
    return {
        "message": "Task deleted successfully"
    }

#Tag creation
@app.post("/tags/", response_model=TagResponse)
def create_tag(
        tag: TagCreate,
        db: Session = Depends(get_db)
):
    new_tag = Tag(
        tag_name=tag.tag_name
    )
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag

#Tag for tasks
@app.post("/tasks/{task_id}/tags/{tag_id}")
def assign_tag(
        task_id: int,
        tag_id: int,
        db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()
    tag = db.query(Tag).filter(
        Tag.id == tag_id
    ).first()
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    if tag is None:
        raise HTTPException(
            status_code=404,
            detail="Tag not found"
        )
    task.tags.append(tag)
    db.commit()

    return {
        "message": "Tag assigned successfully"
    }

#get tags
@app.get("/tasks/{task_id}/tags",
         response_model=list[TagResponse])
def get_task_tags(
        task_id: int,
        db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return task.tags

@app.get("/tags/{tag_id}/tasks",
         response_model=list[TaskResponse])
def get_tag_tasks(
        tag_id: int,
        db: Session = Depends(get_db)
):
    tag = db.query(Tag).filter(
        Tag.id == tag_id
    ).first()

    if tag is None:
        raise HTTPException(
            status_code=404,
            detail="Tag not found"
        )
    return tag.tasks