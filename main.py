from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from database_postgres import Base, get_db, engine
import models, schemas, crud


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/", response_model=list[schemas.Book])
async def read_all_book(db: Annotated[Session, Depends(get_db)]):
    books = crud.get_all_books(db)
    return books


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