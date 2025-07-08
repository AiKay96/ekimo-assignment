import os
from dataclasses import dataclass

@dataclass
class Settings:
    database_url: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://dbuser:password123@localhost:5432/product"
    )
    
    secret_key: str = os.getenv(
        "SECRET_KEY", 
        "your-secret-key"
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


settings = Settings()