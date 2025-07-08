from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass
class Product:
    id: int
    name: str
    price: float
    quantity: float
    last_updated: datetime


class ProductRepository(Protocol):
    def create_many(self, products: list[Product]) -> None:
        pass

    def update_many(self, products: list[Product]) -> None:
        pass
