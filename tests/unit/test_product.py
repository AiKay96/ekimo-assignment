from typing import Any

from src.infra.models.product import Product
from src.infra.repositories.products import ProductRepository
from tests.fake import Fake


def test_should_update_product(db_session: Any) -> None:
    repo = ProductRepository(db_session)

    product = Fake().product()
    repo.update_many([product])
    db_product = db_session.query(Product).filter_by(barcode=product.barcode).first()

    assert db_product is not None
    assert db_product.name == product.name

    updated = Fake().product()
    updated.barcode = product.barcode

    repo.update_many([updated])
    db_product = db_session.query(Product).filter_by(barcode=product.barcode).first()

    assert db_product.name == updated.name


def test_should_read_all_products(db_session: Any) -> None:
    repo = ProductRepository(db_session)

    product1 = Fake().product()
    product2 = Fake().product()
    repo.update_many([product1, product2])

    products = repo.read_all()
    barcodes = {p.barcode for p in products}

    assert product1.barcode in barcodes
    assert product2.barcode in barcodes
