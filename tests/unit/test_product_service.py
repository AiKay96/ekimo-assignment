from typing import Any

import pytest

from src.infra.repositories.products import ProductRepository
from src.infra.services.product import ProductService
from tests.fake import Fake


@pytest.fixture
def product_1() -> Any:
    return Fake().product()


@pytest.fixture
def product_2() -> Any:
    return Fake().product()


@pytest.fixture
def product_service(db_session: Any) -> ProductService:
    repo = ProductRepository(db_session)
    return ProductService(repo)


def test() -> None:
    assert True
