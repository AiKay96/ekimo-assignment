from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.runner.config import settings
from src.runner.db import Base
from src.runner.setup import get_db, init_app

url="postgresql://admin:admin@localhost:5432/ana"
engine = create_engine(url, future=True)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture(scope="session", autouse=True)
def setup_db() -> Any:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session() -> Any:
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session: Any) -> TestClient:
    app = init_app()
    app.dependency_overrides[get_db] = lambda: db_session
    return TestClient(app)
