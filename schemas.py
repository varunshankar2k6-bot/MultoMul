from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    name: str


class StudentCreate(BaseModel):
    name: str
    email: str
    department_id: int


class StudentProfileCreate(BaseModel):
    address: str
    phone: str


class CourseCreate(BaseModel):
    title: str


class CourseResponse(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class StudentResponse(BaseModel):
    id: int
    name: str
    courses: list[CourseResponse] = []

    class Config:
        from_attributes = True