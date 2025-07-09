from dataclasses import dataclass, field
from typing import Any

from faker import Faker

from src.core.products import Product
from src.core.users import User


@dataclass
class Fake:
    faker: Faker = field(default_factory=Faker)

    def user_dict(self) -> dict[str, Any]:
        return {
            "username": self.faker.user_name(),
            "password": self.faker.password(),
        }

    def user(self) -> User:
        data = self.user_dict()
        return User(**data)

    def product_dict(self) -> dict[str, Any]:
        return {
            "name": self.faker.word(),
            "price": self.faker.pydecimal(left_digits=3, right_digits=2, positive=True),
            "quantity": self.faker.pydecimal(
                left_digits=2, right_digits=0, positive=True
            ),
            "last_updated": self.faker.date_time_this_year(),
            "barcode": self.faker.random_int(min=1000000000, max=9999999999),
            "is_synced": self.faker.boolean(),
        }

    def product(self) -> Any:
        data = self.product_dict()
        return Product(**data)
