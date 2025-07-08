from sqlalchemy.orm import Session
from src.core.products import Product, ProductRepository
from src.infra.models.product import ProductModel


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def update_many(self, products: list[Product]) -> None:
        for product in products:
            try:
                existing = self.db.query(ProductModel).filter_by(id=p.id).first()
                if existing:
                    existing.name = p.name
                    existing.price = p.price
                    existing.quantity = p.quantity
                    existing.last_updated = p.last_updated
                else:
                    self.db.add(db_product)
                self.db.commit()
            except SQLAlchemyError:
                self.db.rollback()
