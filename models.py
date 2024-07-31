from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database_postgres import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    # books = relationship("Book", back_populates="uploader")


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    year = Column(Integer, nullable=False)

    # uploaded_by = Column(Integer, ForeignKey(User.id))
    #
    # uploader = relationship("User", back_populates="books")


