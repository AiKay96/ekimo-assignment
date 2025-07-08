from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Protocol


@dataclass
class Product:
    id: int
    name: str
    price: Decimal
    quantity: Decimal
    last_updated: datetime
    barcode: int


class ProductRepository(Protocol):
    def update_many(self, products: list[Product]) -> None:
        pass
