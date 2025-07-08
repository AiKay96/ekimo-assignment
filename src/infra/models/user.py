from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from src.runner.setup import Base


class User(Base):  # type: ignore
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
