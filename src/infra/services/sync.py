from dataclasses import dataclass

import requests

from src.infra.services.product import ProductService
from src.runner.config import settings


@dataclass
class ProductSynchronization:
    service: ProductService

    def _auth(self) -> str:
        response = requests.post(
            f"{settings.base_url}auth",
            data={
                "username": settings.username,
                "password": settings.password,
            },
        )
        return str(response.json()["access_token"])

    def sync(self) -> None:
        unsynced = self.service.read_unsyched_products()
        if not unsynced:
            return

        token = self._auth()
        payload = [
            {
                "id": product.id,
                "name": product.name,
                "price": str(product.price),
                "quantity": str(product.quantity),
                "last_updated": product.last_updated.isoformat(),
                "barcode": product.barcode,
            }
            for product in unsynced
        ]

        response = requests.post(
            f"{settings.base_url}products",
            json={"products": payload},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
