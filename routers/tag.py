from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Task, Tag
from schemas import TagCreate, TagResponse, TaskResponse
router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Creating tag
@router.post("/",
             response_model=TagResponse)
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

# Assigning tag to task
@router.post("/{task_id}/{tag_id}")
def assign_tag(
        task_id: int,
        tag_id: int,
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
    tag = db.query(Tag).filter(
        Tag.id == tag_id
    ).first()
    if not tag:
        raise HTTPException(
            status_code=404,
            detail="Tag not found"
        )
    task.tags.append(tag)
    db.commit()
    return {
        "message": "Tag assigned successfully"
    }

# Displaying tags of a specific task
@router.get("/{task_id}/tags",
            response_model=list[TagResponse])
def get_task_tags(
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
    return task.tags