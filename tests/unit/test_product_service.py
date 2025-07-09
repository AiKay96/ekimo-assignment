from datetime import datetime
from decimal import Decimal
from typing import Any

import pytest

from src.core.products import Product
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


def test_filter_products_should_add_new(
    product_service: ProductService, product_1: Product, product_2: Product
) -> None:
    update = Fake().product()

    updated = product_service._filter_updated_or_new(
        [product_1, product_2],
        [product_1, product_2, update],
    )
    assert len(updated) == 1
    assert updated[0].barcode == update.barcode


def test_filter_products_should_detect_change(
    product_service: ProductService, product_1: Product, product_2: Product
) -> None:
    update = Fake().product()
    update.barcode = product_1.barcode
    updated = product_service._filter_updated_or_new(
        [product_1, product_2],
        [update, product_2],
    )
    assert len(updated) == 1
    assert updated[0].barcode == update.barcode
    assert updated[0].name == update.name
    assert updated[0].price == update.price
    assert updated[0].quantity == update.quantity
    assert updated[0].last_updated == update.last_updated


def test_has_changed() -> None:
    old = Product("A", Decimal("1"), Decimal("1"), datetime.now(), barcode=1)
    same = Product("A", Decimal("1"), Decimal("1"), datetime.now(), barcode=1)
    changed = Product("B", Decimal("2"), Decimal("1"), datetime.now(), barcode=1)

    assert not ProductService._has_changed(same, old)
    assert ProductService._has_changed(changed, old)
