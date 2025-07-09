from dataclasses import dataclass
from decimal import Decimal
from io import BytesIO

import pandas

from src.core.products import Product, ProductRepository


@dataclass
class ProductService:
    repo: ProductRepository

    def parse_and_update(self, file: BytesIO, filename: str) -> None:
        df = self._read_file(file, filename)
        products = self._parse_products(df)
        self.repo.update_many(products)

    def filter_products(self, file: BytesIO, filename: str) -> list[Product]:
        df = self._read_file(file, filename)
        source = self._parse_products(df)
        target = self.repo.read_all()
        return self._filter_updated_or_new(target, source)

    @staticmethod
    def _read_file(file: BytesIO, filename: str) -> pandas.DataFrame:
        if filename.endswith(".csv"):
            return pandas.read_csv(file)
        if filename.endswith(".xlsx"):
            return pandas.read_excel(file)
        raise ValueError("Unsupported file format")

    @staticmethod
    def _parse_products(df: pandas.DataFrame) -> list[Product]:
        return [
            Product(
                name=row["name"],
                price=Decimal(str(row["price"])),
                quantity=Decimal(str(row["quantity"])),
                last_updated=pandas.to_datetime(row["last_updated"]),
                barcode=row["barcode"],
            )
            for _, row in df.iterrows()
        ]

    @staticmethod
    def _filter_updated_or_new(
        target: list[Product], source: list[Product]
    ) -> list[Product]:
        target_map = {product.barcode: product for product in target}

        return [
            product
            for product in source
            if (target_product := target_map.get(product.barcode)) is None
            or ProductService._has_changed(product, target_product)
        ]

    @staticmethod
    def _has_changed(product_1: Product, product_2: Product) -> bool:
        return product_1.barcode == product_2.barcode and (
            product_1.name != product_2.name
            or product_1.price != product_2.price
            or product_1.quantity != product_2.quantity
        )
