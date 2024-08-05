from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
from sqlalchemy.sql import crud

import models
import schemas
import utils
import database_postgres

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "7b001efbdceef2fdf30c51a42916e2f5b2fd04124cb4d5d382a0ec813417783c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def login(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid email or password")
    if not utils.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid email or password")

    return user


def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt


def verify_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credential_exception
        token_data = schemas.TokenData(user_id=user_id)
    except InvalidTokenError:
        raise credential_exception
    return token_data


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(database_postgres.get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token_data = verify_token(token, credential_exception)
    # used the db session rather than the get_user function
    user = db.query(models.User).filter(models.User.id == token_data.user_id).first()
    if user is None:
        raise credential_exception
    return user


def get_current_active_admin(current_user: schemas.User = Depends(get_current_user)):
    if current_user.role.name != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session):
    users = db.query(models.User).all()
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no users. Create One.")
    return users


def create_user(user: schemas.UserCreate, db: Session):
    hashed_password: str = utils.hash_password(user.password)
    role = db.query(models.Role).filter(models.Role.name == user.role_name).first()
    db_user = models.User(email=user.email, hashed_password=hashed_password, role_id=role.id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user




def get_all_books(db: Session):
    # to return books to a user that were created by that user .filter(models.Book.uploader_id == user_id)
    return db.query(models.Book).all()


def get_book(book_id: int, db: Session):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id: {book_id} not found")
    else:
        return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book(book: schemas.BookCreate, db: Session, user_id: int):
    db_book = models.Book(**book.model_dump(), uploader_id=user_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return f"book successfully created"


def update_book(book_id: int, book: schemas.BookCreate, db: Session, user_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id: {book_id} not found")
    else:
        if db_book.uploader_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"You can not edit this book.")
        db_book.title = book.title
        db_book.author = book.author
        db_book.year = book.year
        db.commit()
        db.refresh(db_book)
        return f"book successfully updated"


def delete_book(book_id: int, db: Session, user_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id: {book_id} not found")
    else:
        if db_book.uploader_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"You can not delete this book.")
        db.delete(db_book)
        db.commit()
        return "book deleted"
