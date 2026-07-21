import re
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.user import User

from app.auth.hashing import verify_password
from app.auth.jwt import create_access_token
from app.auth.dependencies import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


from sqlalchemy import func
from pydantic import BaseModel, EmailStr
from app.auth.hashing import verify_password, hash_password


class UserProfileUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None


class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    username: str
    password: str
    role: str = "Clinician"


# -------------------------------------------------------
# LOGIN (SUPPORTING EMAIL OR USERNAME)
# -------------------------------------------------------
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    submitted_identifier = form_data.username.strip()

    if not submitted_identifier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide a valid username or email address"
        )

    # Query by User.email OR User.username (case-insensitive)
    user = (
        db.query(User)
        .filter(
            (func.lower(User.email) == submitted_identifier.lower()) |
            (func.lower(User.username) == submitted_identifier.lower())
        )
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email/username or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive. Please contact an administrator."
        )

    if not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email/username or password"
        )

    access_token = create_access_token(
        {
            "sub": user.username
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# -------------------------------------------------------
# PUBLIC USER REGISTRATION
# -------------------------------------------------------
@router.post("/register")
def register(
    data: UserRegister,
    db: Session = Depends(get_db)
):
    clean_username = data.username.strip().lower()
    clean_email = data.email.strip().lower()

    if db.query(User).filter(func.lower(User.username) == clean_username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken. Please choose another."
        )

    if db.query(User).filter(func.lower(User.email) == clean_email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address is already registered. Please login instead."
        )

    allowed_roles = ["Admin", "Clinician", "Researcher"]
    user_role = data.role.strip() if data.role else "Clinician"
    if user_role not in allowed_roles:
        user_role = "Clinician"

    new_user = User(
        username=clean_username,
        email=clean_email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name.strip(),
        role=user_role,
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token({"sub": new_user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "full_name": new_user.full_name,
            "role": new_user.role,
            "is_active": new_user.is_active
        }
    }



# -------------------------------------------------------
# CURRENT USER
# -------------------------------------------------------
@router.get("/me")
def get_logged_in_user(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_active": current_user.is_active
    }


# -------------------------------------------------------
# UPDATE CURRENT USER PROFILE
# -------------------------------------------------------
@router.put("/me")
def update_logged_in_user(
    profile_data: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if profile_data.full_name is not None:
        current_user.full_name = profile_data.full_name.strip()

    if profile_data.email is not None and profile_data.email.strip() != "":
        current_user.email = profile_data.email.strip().lower()

    db.commit()
    db.refresh(current_user)

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_active": current_user.is_active
    }