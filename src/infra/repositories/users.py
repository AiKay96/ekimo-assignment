from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.core.errors import ExistsError
from src.core.users import User
from src.infra.models.user import User as UserModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> None:
        if self.db.query(UserModel).filter_by(username=user.username).first():
            raise ExistsError

        db_user = UserModel(
            username=user.username,
            hashed_password=pwd_context.hash(user.password),
            id=user.id,
        )
        self.db.add(db_user)
        self.db.commit()
