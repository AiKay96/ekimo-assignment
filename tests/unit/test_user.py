from typing import Any

import pytest

from src.core.errors import ExistsError
from src.infra.models.user import User as UserModel
from src.infra.repositories.users import UserRepository
from tests.fake import Fake


def test_user_repository_create(db_session: Any) -> None:
    repo = UserRepository(db_session)
    user = Fake().user()

    repo.create(user)
    db_user = db_session.query(UserModel).filter_by(username=user.username).first()

    assert db_user is not None
    assert db_user.username == user.username


def test_user_create_duplicate_raises_exists_error(db_session: Any) -> None:
    repo = UserRepository(db_session)

    user = Fake().user()
    repo.create(user)

    with pytest.raises(ExistsError):
        repo.create(user)
