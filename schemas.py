from pydantic import BaseModel, Field
from typing import Annotated


class BookBase(BaseModel):
    title: Annotated[str, Field(max_length=100)]
    author: str
    year: Annotated[int, Field(le=2024)]


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int

    class Config:
        from_attributes = True
