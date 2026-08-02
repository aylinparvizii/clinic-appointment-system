from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Literal

class UserRegister(BaseModel):
    first_name: str
    last_name: str
    mobile: str
    email: EmailStr
    password: str
    role: Literal["doctor","patient"]
    gender: str | None = None
    birth_date: date | None = None


class UserLogin(BaseModel):
    mobile: str
    password: str


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    mobile: str
    email: str
    role: str
    gender: str | None = None
    birth_date: date | None = None
    is_active: bool

    class Config:
        from_attributes = True