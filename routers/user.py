from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
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

#user signup
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
    )