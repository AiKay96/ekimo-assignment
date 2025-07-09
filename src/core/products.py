from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Protocol
from uuid import uuid4


@dataclass
class Product:
    name: str
    price: Decimal
    quantity: Decimal
    last_updated: datetime
    barcode: int
    is_synched: bool = False

    id: int = field(default_factory=lambda: uuid4().int >> 64)


class ProductRepository(Protocol):
    def update_many(self, products: list[Product]) -> None:
        pass

    def read_many_unsynched(self) -> list[Product]:
        pass
