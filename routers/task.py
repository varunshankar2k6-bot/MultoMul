from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, Task
from schemas import TaskCreate, TaskResponse
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Adding task for user
@router.post("/{user_id}",
             response_model=TaskResponse)
def add_task(
        user_id: int,
        task: TaskCreate,
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()
    if not user:
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

# Displaying all tasks of user
@router.get("/{user_id}",
            response_model=list[TaskResponse])
def get_tasks(
        user_id: int,
        db: Session = Depends(get_db)
):
    return db.query(Task).filter(
        Task.user_id == user_id
    ).all()

# Displaying pending tasks
@router.get("/{user_id}/pending",
            response_model=list[TaskResponse])
def get_pending_tasks(
        user_id: int,
        db: Session = Depends(get_db)
):
    return db.query(Task).filter(
        Task.user_id == user_id,
        Task.completed == False
    ).all()

# Marking task completed
@router.put("/{task_id}/complete",
            response_model=TaskResponse)
def complete_task(
        task_id: int,
        db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    task.completed = True
    db.commit()
    db.refresh(task)
    return task

# Deleting task
@router.delete("/{task_id}")
def delete_task(
        task_id: int,
        db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    db.delete(task)
    db.commit()
    return {
        "message": "Task deleted successfully"
    }