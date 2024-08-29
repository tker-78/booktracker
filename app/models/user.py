from sqlalchemy import String, Integer, Column, Boolean, DateTime
from datetime import datetime

from models.base import Base, session_scope


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime)
    disabled = Column(Boolean)



    @classmethod
    def create(cls, id, username, email, hashed_password, created_at, disabled):
        user = cls(id=id, username=username, email=email, hashed_password=hashed_password, created_at=created_at, disabled=disabled)
        try:
            with session_scope() as session:
                session.add(user)
        except Exception as e:
            print(f"error: {e}")

    @classmethod
    def get(cls, id):
        with session_scope() as session:
            user = session.query(cls).filter(cls.id == id).first()
        if user is None:
            return None
        return user

    @classmethod
    def get_by_username(cls, username):
        with session_scope() as session:
            user = session.query(cls).filter(cls.username == username).first()
        if user is None:
            return None
        return user
        