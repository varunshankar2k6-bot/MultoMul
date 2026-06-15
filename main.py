from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import Department, Student, StudentProfile, Course
from schemas import *

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Welcome"}


@app.post("/departments")
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db)
):

    db_department = Department(
        name=department.name
    )

    db.add(db_department)
    db.commit()
    db.refresh(db_department)

    return db_department


@app.post("/students")
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):

    db_student = Student(
        name=student.name,
        email=student.email,
        department_id=student.department_id
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student


@app.post("/students/{student_id}/profile")
def create_profile(
    student_id: int,
    profile: StudentProfileCreate,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db_profile = StudentProfile(
        address=profile.address,
        phone=profile.phone,
        student_id=student_id
    )

    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)

    return db_profile


@app.post("/courses")
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):

    db_course = Course(
        title=course.title
    )

    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course


@app.post("/students/{student_id}/courses/{course_id}")
def enroll_student(
    student_id: int,
    course_id: int,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    student.courses.append(course)

    db.commit()

    return {
        "message": "Enrollment successful"
    }


@app.get(
    "/students/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    return db.query(Student).filter(
        Student.id == student_id
    ).first()


@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully"
    }