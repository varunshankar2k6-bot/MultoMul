from fastapi import FastAPI
from database import engine, Base
from routers import user, task, tag
app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(
    user.router,
    prefix="/users",
    tags=["Users"]
)
app.include_router(
    task.router,
    prefix="/tasks",
    tags=["Tasks"]
)
app.include_router(
    tag.router,
    prefix="/tags",
    tags=["Tags"]
)