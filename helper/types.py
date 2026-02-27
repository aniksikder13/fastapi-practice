from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class BookResponse(BaseModel):
    id: int
    name: str
    price: float
    rating: float
    author: str
    summery: str
    category: str
    publish_date: datetime


class BookCreate(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="ID is not needed on create"
    )
    name: str = Field(min_length=5)
    price: float = Field(gt=0)
    rating: float = Field(gt=0, lt=6)
    author: str = Field(min_length=5)
    summery: str = Field(min_length=15, max_length=120)
    category: str = Field(min_length=3)
    publish_date: datetime

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "A New Book",
                "author": "Writer x",
                "summery": "A new description of a book",
                "category": "xxx",
                "price": 10,
                "rating": 5,
                "publish_date": "xxxx-xx-xx"
            }
        }
    }


class BookUpdate(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None
    summery: Optional[str] = None
    rating: Optional[float] = None
    category: Optional[str] = None
    publish_date: Optional[datetime] = None