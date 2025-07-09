from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.runner.db import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    last_updated: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    barcode: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    is_synced: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    def __init__(
        self,
        name: str,
        price: Decimal,
        quantity: Decimal,
        last_updated: datetime,
        barcode: int,
        is_synced: bool = False,
    ) -> None:
        self.name = name
        self.price = price
        self.quantity = quantity
        self.last_updated = last_updated
        self.barcode = barcode
        self.is_synced = is_synced
