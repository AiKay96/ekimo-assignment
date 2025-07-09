from dataclasses import dataclass

import bcrypt
from sqlalchemy.orm import Session

from src.core.errors import DoesNotExistError, ExistsError
from src.core.users import User
from src.infra.models.user import User as UserModel


@dataclass
class UserRepository:
    db: Session

    def create(self, user: User) -> None:
        if self.db.query(UserModel).filter_by(username=user.username).first():
            raise ExistsError

        db_user = UserModel(
            username=user.username,
            hashed_password=bcrypt.hashpw(
                user.password.encode(), bcrypt.gensalt()
            ).decode(),
            user_id=user.id,
        )
        self.db.add(db_user)
        self.db.commit()

    def read(self, username: str) -> User:
        user = self.db.query(UserModel).filter_by(username=username).first()
        if not user:
            raise DoesNotExistError
        assert user.id is not None
        assert user.username is not None
        assert user.hashed_password is not None

        return User(
            id=user.id,
            username=user.username,
            password=user.hashed_password,
        )
