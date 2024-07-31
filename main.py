from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database_postgres import Base, get_db, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/", response_model=list[schemas.Book])
async def read_all_book(db: Annotated[Session, Depends(get_db)]):
    books = crud.get_all_books(db)
    return books


@app.post("/login", response_model=schemas.Token)
async def login(db: Session = Depends(get_db), user_credentials: OAuth2PasswordRequestForm = Depends()):
    user = crud.login(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"})
    access_token = crud.create_token({"user_id": user.id})
    return schemas.Token(access_token=access_token, token_type="bearer")


@app.get("/{book_id}", response_model=schemas.Book)
async def read_book(book_id: int, db: Annotated[Session, Depends(get_db)]):
    return crud.get_book(book_id, db)


@app.post("/books")
async def create_book(book: schemas.BookCreate, db: Annotated[Session, Depends(get_db)]):
    return crud.create_book(book, db)


@app.put("/books/{book_id}")
async def update_book(book_id: int, book: schemas.BookCreate, db: Annotated[Session, Depends(get_db)]):
    return crud.update_book(book_id, book, db)


@app.delete("/books/{book_id}")
async def delete_book(book_id: int, db: Annotated[Session, Depends(get_db)]):
    return crud.delete_book(book_id, db)


@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    return crud.get_user(user_id, db)


@app.post("/users", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]):
    new_user = crud.get_user_by_email(db, user.email)

    if new_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.create_user(user, db)
