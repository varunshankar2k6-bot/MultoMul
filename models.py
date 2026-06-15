from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


# ---------------- USER ----------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    tasks = relationship("Task", back_populates="user")


# ---------------- TASK ----------------
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    completed = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tasks")

    task_detail = relationship(
        "TaskDetail",
        back_populates="task",
        uselist=False
    )

    tags = relationship("Tag", back_populates="task")


# ---------------- TASK DETAIL ----------------
class TaskDetail(Base):
    __tablename__ = "task_details"

    id = Column(Integer, primary_key=True)
    description = Column(String)
    due_date = Column(String)

    task_id = Column(Integer, ForeignKey("tasks.id"), unique=True)

    task = relationship("Task", back_populates="task_detail")


# ---------------- TAG ----------------
class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    tag_name = Column(String)

    task_id = Column(Integer, ForeignKey("tasks.id"))

    task = relationship("Task", back_populates="tags")