from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
from decimal import Decimal


@dataclass
class Product:
    id: int
    name: str
    price: Decimal
    quantity: Decimal
    last_updated: datetime


class ProductRepository(Protocol):
    def create_many(self, products: list[Product]) -> None:
        pass

    def update_many(self, products: list[Product]) -> None:
        pass
