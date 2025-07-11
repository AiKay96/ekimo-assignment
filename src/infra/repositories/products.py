from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.core.products import Product
from src.infra.models.product import Product as ProductModel


@dataclass
class ProductRepository:
    db: Session

    def update_many(self, products: list[Product]) -> None:
        try:
            new_products = []

            for product in products:
                existing = (
                    self.db.query(ProductModel)
                    .filter_by(barcode=product.barcode)
                    .first()
                )
                if existing:
                    existing.name = product.name
                    existing.price = product.price
                    existing.quantity = product.quantity
                    existing.last_updated = datetime.utcnow()
                else:
                    product_model = ProductModel(
                        name=product.name,
                        price=product.price,
                        quantity=product.quantity,
                        last_updated=datetime.utcnow(),
                        barcode=product.barcode,
                    )
                    new_products.append(product_model)

            if new_products:
                self.db.add_all(new_products)

            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()

    def read_many_unsynched(self) -> list[Product]:
        products = self.db.query(ProductModel).filter_by(is_synced=False).all()
        return [
            Product(
                id=product.id,
                name=product.name,
                price=product.price,
                quantity=product.quantity,
                last_updated=product.last_updated,
                barcode=product.barcode,
                is_synched=product.is_synced,
            )
            for product in products
        ]

    def mark_as_synced(self, products: list[Product]) -> None:
        try:
            unsynced_models = (
                self.db.query(ProductModel).filter_by(is_synced=False).all()
            )
            unsynced_map = {model.barcode: model for model in unsynced_models}
            for product in products:
                model = unsynced_map.get(product.barcode)
                if model:
                    model.is_synced = True
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
