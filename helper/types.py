import uuid
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date, datetime
from enum import Enum

class UserRole(str, Enum):
    user = "user"
    admin = "admin"


class UserResponse(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    date_of_birth: date
    role: UserRole
    id: uuid.UUID
    created_at: datetime


class UserCreateRequest(BaseModel):
    first_name: str = Field(min_length=3, max_length=80)
    last_name: str = Field(min_length=3, max_length=80)
    email: EmailStr
    password: str = Field(min_length=6)
    date_of_birth: date
    role: UserRole


class TodoCreateRequest(BaseModel):
    title: str = Field(min_length=3, max_length=80)
    description: str = Field(min_length=3, max_length=120)
    priority: int = Field(gt=0, lt=6)
    is_completed: Optional[bool] = None


class TodoUpdateRequest(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=80)
    description: Optional[str] = Field(default=None, min_length=3, max_length=120)
    priority: Optional[int] = Field(default=None, gt=0, lt=6)
    is_completed: Optional[bool] = None
