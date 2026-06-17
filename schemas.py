from pydantic import BaseModel
#user
class UserCreate(BaseModel):
    name: str
    email: str
    username: str
    password: str
    role: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    username: str
    role: str
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


#task
class TaskCreate(BaseModel):
    title: str

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    user_id: int
    class Config:
        from_attributes = True

#tag
class TagCreate(BaseModel):
    tag_name: str

class TagResponse(BaseModel):
    id: int
    tag_name: str
    class Config:
        from_attributes = True