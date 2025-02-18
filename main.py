from typing import Annotated, Any

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud
import schemas
from database_postgres import Base, get_db, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/", response_model=list[schemas.Book])
async def read_all_book(
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(crud.get_current_user),
        ):
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


@app.get("/books/{book_id}", response_model=schemas.Book)
async def read_book(book_id: int, db: Annotated[Session, Depends(get_db)]):
    return crud.get_book(book_id, db)


@app.post("/books")
# used int as the type hint for current_user
async def create_book(
        book: schemas.BookCreate,
        db: Annotated[Session, Depends(get_db)],
        current_user: schemas.User = Depends(crud.get_current_user),
):
    return crud.create_book(book, db, user_id=current_user.id)


@app.put("/books/{book_id}")
async def update_book(
        book_id: int,
        book: schemas.BookCreate,
        db: Annotated[Session, Depends(get_db)],
        current_user: schemas.User = Depends(crud.get_current_user),
):
    return crud.update_book(book_id, book, db, user_id=current_user.id)


@app.delete("/books/{book_id}")
async def delete_book(
        book_id: int,
        db: Annotated[Session, Depends(get_db)],
        current_user: schemas.User = Depends(crud.get_current_user),
):
    return crud.delete_book(book_id, db, user_id=current_user.id)


@app.get("/users", response_model=list[schemas.User])
async def read_user(
        db: Annotated[Session, Depends(get_db)],
        current_user: schemas.User = Depends(crud.get_current_active_admin)
):
    return crud.get_users(db)


@app.post("/users", response_model=schemas.User)
async def create_user(
        user: schemas.UserCreate,
        db: Annotated[Session, Depends(get_db)],
        current_user: schemas.User = Depends(crud.get_current_active_admin)):

    new_user = crud.get_user_by_email(db, user.email)

    if new_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.create_user(user, db)

