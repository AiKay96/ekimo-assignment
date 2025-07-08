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
                existing = (
                    self.db.query(ProductModel)
                    .filter_by(barcode=product.barcode)
                    .first()
                )
                if existing:
                    existing.name = product.name
                    existing.price = product.price
                    existing.quantity = product.quantity
                    existing.last_updated = product.last_updated
                else:
                    product_model = ProductModel(
                        name=product.name,
                        price=product.price,
                        quantity=product.quantity,
                        last_updated=product.last_updated,
                        barcode=product.barcode,
                    )
                    self.db.add(product_model)
                self.db.commit()
            except SQLAlchemyError:
                self.db.rollback()
