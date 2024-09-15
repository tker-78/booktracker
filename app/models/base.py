from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from contextlib import contextmanager

import threading

Base = declarative_base()

# engine = create_engine('postgresql://ユーザー名:パスワード@ホスト:ポート/データベース名')
engine = create_engine(f'postgresql+psycopg2://postgres:postgres@postgres_db_container/postgres_db')

Session = scoped_session(sessionmaker(bind=engine))

lock = threading.Lock()

@contextmanager
def session_scope():
    session = Session()
    session.expire_on_commit = False

    try:
        lock.acquire()
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        lock.release()

def init_db():
    # __init__.pyから呼び出す
    import models.user
    import models.book
    Base.metadata.create_all(bind=engine)
    print("database initialized..")
    






