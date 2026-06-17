from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Table
)
from sqlalchemy.orm import relationship
from database import Base


#Many to many
task_tag = Table(
    "task_tag",
    Base.metadata,
    Column(
        "task_id",
        Integer,
        ForeignKey("tasks.id"),
        primary_key=True
    ),
    Column(
        "tag_id",
        Integer,
        ForeignKey("tags.id"),
        primary_key=True
    )
)

#user details
class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    name = Column(String(100))
    email = Column(
        String(100),
        unique=True
    )
    username = Column(
        String(100),
        unique=True
    )
    password = Column(String(255))
    role = Column(String(50))
    tasks = relationship(
        "Task",
        back_populates="user"
    )

#task details
class Task(Base):
    __tablename__ = "tasks"
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    title = Column(String(200))
    completed = Column(
        Boolean,
        default=False
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )
    user = relationship(
        "User",
        back_populates="tasks"
    )
    tags = relationship(
        "Tag",
        secondary=task_tag,
        back_populates="tasks"
    )

#Tag details
class Tag(Base):
    __tablename__ = "tags"
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    tag_name = Column(
        String(100),
        unique=True
    )
    tasks = relationship(
        "Task",
        secondary=task_tag,
        back_populates="tags"
    )