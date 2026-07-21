from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):

    username: str

    email: EmailStr

    password: str

    full_name: str

    role: str = "Clinician"


class UserLogin(BaseModel):

    username: str

    password: str


class UserResponse(BaseModel):

    id: int

    username: str

    email: EmailStr

    full_name: str

    role: str

    is_active: bool

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):

    full_name: str | None = None

    email: EmailStr | None = None

    role: str | None = None

    is_active: bool | None = None