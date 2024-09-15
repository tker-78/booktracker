import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base

# テスト用のデータベースエンジンを作成
@pytest.fixture(scope="module")
def test_engine():
    test_engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(test_engine)
    return test_engine

# テスト用のセッションを作成
@pytest.fixture(scope="function")
def session(test_engine):
    Session = sessionmaker(test_engine)
    session = Session()
    yield session
    session.close()