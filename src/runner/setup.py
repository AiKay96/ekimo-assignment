from collections.abc import Generator

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.infra.fastapi.auth import auth_api
from src.infra.fastapi.products import product_api
from src.infra.fastapi.users import user_api
from src.infra.repositories.products import ProductRepository
from src.infra.repositories.users import UserRepository
from src.infra.services.product import ProductService
from src.infra.services.sync import ProductSynchronization
from src.runner.config import settings
from src.runner.db import Base

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)

    app = FastAPI()
    app.include_router(user_api)
    app.include_router(auth_api)
    app.include_router(product_api)

    db: Session = next(get_db())
    app.state.users = UserRepository(db)
    app.state.products = ProductRepository(db)

    @app.on_event("startup")
    def start_sync_scheduler() -> None:
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            init_sync().sync, "interval", minutes=settings.sync_interval_minutes
        )
        scheduler.start()
        app.state.scheduler = scheduler

    @app.on_event("shutdown")
    def stop_sync_scheduler() -> None:
        scheduler = app.state.scheduler
        scheduler.shutdown(wait=False)

    return app


def init_sync() -> ProductSynchronization:
    db: Session = next(get_db())
    return ProductSynchronization(ProductService(ProductRepository(db)))
