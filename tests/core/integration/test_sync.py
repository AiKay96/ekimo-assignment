from unittest.mock import MagicMock, patch

import pytest

from src.core.products import Product
from src.infra.services.product import ProductService
from src.infra.services.sync import ProductSynchronization
from tests.fake import Fake


@pytest.fixture
def product() -> Product:
    return Fake().product()


@pytest.fixture
def product_service(product: Product) -> MagicMock:
    service = MagicMock(spec=ProductService)
    service.read_unsyched_products.return_value = [product]
    return service


def test_sync_sends_data(product_service: MagicMock, product: Product) -> None:
    sync = ProductSynchronization(service=product_service)

    with patch("src.infra.services.sync.requests.post") as mock_post:
        mock_post.side_effect = [
            MagicMock(status_code=200, json=lambda: {"access_token": "fake-token"}),
            MagicMock(status_code=201),
        ]

        sync.sync()
        assert mock_post.call_count == 2

        auth_call = mock_post.call_args_list[0]
        assert "auth" in auth_call[0][0]

        product_call = mock_post.call_args_list[1]
        assert "products" in product_call[0][0]
        assert product_call[1]["headers"]["Authorization"] == "Bearer fake-token"
        assert product_call[1]["json"]["products"][0]["barcode"] == product.barcode
