from datetime import datetime
from decimal import Decimal
from sqlalchemy import Integer, String, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from src.runner.db import Base


class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    last_updated: Mapped[datetime] = mapped_column(DateTime, nullable=False)