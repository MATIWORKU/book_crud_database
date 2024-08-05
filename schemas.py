from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Optional
from datetime import datetime


class RoleBase(BaseModel):
    name: str
    permissions: str


class Role(RoleBase):
    id: int

    class Config:
        from_attribute = True


class BookBase(BaseModel):
    title: Annotated[str, Field(max_length=100)]
    author: str
    year: Annotated[int, Field(le=2024)]


class BookCreate(BookBase):
    pass


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role_name: str


class User(UserBase):
    id: int
    created_at: datetime
    role: Optional[Role]

    class Config:
        from_attributes = True


class Book(BookBase):
    id: int
    uploader_id: int
    uploader: Optional[User]

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None


Book.update_forward_refs()
User.update_forward_refs()
