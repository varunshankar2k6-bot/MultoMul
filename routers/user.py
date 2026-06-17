from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from models import User
from schemas import (
    UserCreate,
    UserResponse,
    TokenResponse
)
from database import get_db
from jwt_utils import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)
router = APIRouter()

#user sign up
@router.post(
    "/signup",
    response_model=UserResponse
)
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )
    hashed_password = hash_password(
        user.password
    )
    db_user = User(
        name=user.name,
        email=user.email,
        username=user.username,
        password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#user login
@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.username == form_data.username
    ).first()
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="Invalid username"
        )
    if not verify_password(
        form_data.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )
    token = create_access_token(
        {
            "sub": db_user.username,
            "role": db_user.role
        }
    )
    return {
        "access_token": token,
        "token_type": "bearer"
    }

#getting user details
@router.get("/profile")
def profile(
    current_user: dict = Depends(get_current_user)
):
    return current_user