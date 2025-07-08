from dataclasses import dataclass

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.core.products import Product
from src.infra.models.product import Product as ProductModel


@dataclass
class ProductRepository:
    db: Session

    def update_many(self, products: list[Product]) -> None:
        for product in products:
            try:
                existing = self.db.query(ProductModel).filter_by(barcode=product.barcode).first()
                if existing:
                    existing.name = product.name
                    existing.price = product.price
                    existing.quantity = product.quantity
                    existing.last_updated = product.last_updated
                else:
                    self.db.add(product)
                self.db.commit()
            except SQLAlchemyError:
                self.db.rollback()
