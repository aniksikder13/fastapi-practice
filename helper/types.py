from pydantic import BaseModel, Field
from typing import Optional

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