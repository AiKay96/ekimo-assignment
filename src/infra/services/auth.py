from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from src.core.errors import DoesNotExistError
from src.core.users import UserRepository
from src.runner.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class AuthService:
    users: UserRepository

    def authenticate(self, username: str, password: str) -> Any:
        user = self.users.read(username)
        if not user or not pwd_context.verify(password, user.password):
            raise DoesNotExistError("Invalid credentials")

        payload = {
            "sub": user.username,
            "exp": datetime.utcnow()
            + timedelta(minutes=settings.access_token_expire_minutes),
        }
        return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
