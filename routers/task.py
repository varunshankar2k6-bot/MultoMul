from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Task
from schemas import (
    TaskCreate,
    TaskResponse
)
from jwt_utils import get_current_user
router = APIRouter()

#Adding Task
@router.post(
    "/{user_id}",
    response_model=TaskResponse
)
def add_task(
    user_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_task = Task(
        title=task.title,
        description=task.description,
        user_id=user_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task

#admin access
@router.get(
    "/all"
)
def all_tasks(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    tasks = db.query(Task).all()
    return tasks