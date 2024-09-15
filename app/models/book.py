from sqlalchemy import String, Integer, Column, Boolean, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from datetime import datetime

import requests

from models.base import Base, session_scope
from models.user import User

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String)
    author = Column(String)
    published_at = Column(DateTime)
    category = Column(String)
    cover_image = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


    @classmethod
    def create(cls, id, title, author, published_at, category, cover_image):
        book = cls(id, title, author, published_at, category, cover_image, datetime.now(), datetime.now())
        try:
            with session_scope() as session:
                session.add(book)
        except Exception as e:
            print(e)

    @classmethod
    def get(cls, id):
        with session_scope() as session:
            book = session.query(cls).filter(cls.id == id).first()
        if book is None:
            return None
        return book

    @classmethod
    def update():
        pass

    @classmethod
    def delete():
        pass

    # Google Books APIから情報を取得
    @classmethod
    def get_books_from_google(cls, title: str = None):
        google_books_api_base_url = 'https://www.googleapis.com/books/v1/'
        books = requests.get(google_books_api_base_url + f"volumes?q={title}")
        return books.json()
