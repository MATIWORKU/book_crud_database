from sqlalchemy.orm import Session
import models, schemas


def get_all_books(db: Session):
    return db.query(models.Book).all()


def get_book(book_id: int, db: Session):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        return f"Book {book_id} not found"
    else:
        return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book(book: schemas.BookCreate, db: Session):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return f"book successfully created"


def update_book(book_id: int, book: schemas.BookCreate, db: Session):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        return f"book not found"
    else:
        db_book.title = book.title
        db_book.author = book.author
        db_book.year = book.year
        db.commit()
        db.refresh(db_book)
        return f"book successfully updated"


def delete_book(book_id: int, db: Session):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        return f"book not found"
    else:
        db.delete(db_book)
        db.commit()
        return "book deleted"
