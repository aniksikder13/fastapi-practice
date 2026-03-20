from sqlmodel import Field, SQLModel, Relationship
from uuid import uuid4, UUID
from datetime import datetime, timezone, date
from typing import List, Optional


class User(SQLModel, table=True):

    __tablename__ = "User"

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    first_name: str = Field(max_length=80)
    last_name: str = Field(max_length=80)
    username: str = Field(max_length=15, unique=True, index=True)
    email: str = Field(unique=True)
    phone: str = Field(max_length=12, min_length=11)
    password: str
    date_of_birth: date
    is_active: bool = Field(default=True)
    role: str = Field(default="user")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # 👇 One-to-Many relationship
    todos: List["Todo"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete"}
    )


class Token(SQLModel, table=True):

    __tablename__ = "Token"

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="User.id")
    refresh_token: str
    expire: datetime


class Todo(SQLModel, table=True):

    __tablename__ = "Todo"

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(index=True)
    description: str = Field(max_length=500, min_length=10)
    priority: int = Field(default=1)
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user_id: UUID = Field(foreign_key="User.id")

    # 👇 Many-to-One relationship
    user: Optional[User] = Relationship(back_populates="todos")
