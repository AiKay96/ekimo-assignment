import os
from dataclasses import dataclass


@dataclass
class Settings:
    database_url: str = os.getenv(
        "DATABASE_URL", "postgresql://admin:admin@localhost:5432/ekimo"
    )
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )
    username: str = os.getenv("USERNAME", "admin")
    password: str = os.getenv("PASSWORD", "admin")
    base_url: str = os.getenv("BASE_URL", "http://localhost:8000/")
    sync_interval_minutes: int = int(os.getenv("SYNC_INTERVAL_MINUTES", "10"))


settings = Settings()
