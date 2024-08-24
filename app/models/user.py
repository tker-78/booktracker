from sqlalchemy import String, Integer, Column, Boolean

from models.base import Base, session_scope


class UserList(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


    @classmethod
    def create(cls, id, name, age):
        user = cls(id=id, name=name, age=age)
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