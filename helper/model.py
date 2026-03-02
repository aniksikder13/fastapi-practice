from sqlmodel import Field, SQLModel
from uuid import uuid4, UUID
from datetime import datetime, timezone


class Todo(SQLModel, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))
