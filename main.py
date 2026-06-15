from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import User, Task
from schemas import (
    UserCreate,
    UserResponse,
    TaskCreate,
    TaskResponse
)

app = FastAPI()

Base.metadata.create_all(bind=engine)


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- CREATE USER ----------------
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


# ---------------- GET ALL USERS ----------------
@app.get("/users/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):

    users = db.query(User).all()

    return users


# ---------------- GET USER BY ID ----------------
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# ---------------- ADD TASK FOR USER ----------------
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


# ---------------- GET ALL TASKS OF A USER ----------------
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


# ---------------- GET ONLY PENDING TASKS ----------------
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


# ---------------- MARK TASK AS COMPLETED ----------------
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


# ---------------- DELETE TASK ----------------
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