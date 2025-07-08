import pandas as pd
from io import BytesIO
from src.core.products import Product, ProductRepository
from datetime import datetime
from decimal import Decimal
from dataclasses import dataclass

@dataclass
class ProductService:
    repo: ProductRepository

    def parse_and_update(self, file: BytesIO, filename: str) -> None:
        df = self._read_file(file, filename)
        products = self._parse_products(df)
        self.repo.update_many(products)

    def _read_file(self, file: BytesIO, filename: str) -> pd.DataFrame:
        if filename.endswith(".csv"):
            return pd.read_csv(file)
        elif filename.endswith(".xlsx"):
            return pd.read_excel(file)
        else:
            raise ValueError("Unsupported file format")

    def _parse_products(self, df: pd.DataFrame) -> list[Product]:
        return [
            Product(
                name=row["name"],
                price=Decimal(str(row["price"])),
                quantity=Decimal(str(row["quantity"])),
                last_updated=pd.to_datetime(row["last_updated"]),
                barcode=row.get["barcode"],
            )
            for _, row in df.iterrows()
        ]
