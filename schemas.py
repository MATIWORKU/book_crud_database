from pydantic import BaseModel, Field, EmailStr
from typing import Annotated
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: Annotated[str, Field(max_length=100)]
    author: str
    year: Annotated[int, Field(le=2024)]


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    uploader_id: int
    uploader: User

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None
