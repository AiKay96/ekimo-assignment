from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.infra.fastapi.auth import auth_api
from src.infra.fastapi.products import product_api
from src.infra.fastapi.users import user_api
from src.infra.repositories.products import ProductRepository
from src.infra.repositories.users import UserRepository
from src.runner.config import settings
from src.runner.db import Base
from src.runner.setup import get_db

settings.database_url = settings.database_url + "_test"
engine = create_engine(settings.database_url, future=True)
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
def client(db_session: Session) -> TestClient:
    app = FastAPI()

    app.include_router(user_api)
    app.include_router(auth_api)
    app.include_router(product_api)
    app.dependency_overrides[get_db] = lambda: db_session
    app.state.users = UserRepository(db_session)
    app.state.products = ProductRepository(db_session)

    return TestClient(app)
