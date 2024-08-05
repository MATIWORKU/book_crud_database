from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database_postgres import Base


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False, unique=True, index=True)
    permissions = Column(String, nullable=False)

    users = relationship('User', back_populates='role')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    books = relationship("Book", back_populates="uploader")
    role = relationship("Role", back_populates="users")


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    year = Column(Integer, nullable=False)
    uploader_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)

    uploader = relationship("User", back_populates="books")


