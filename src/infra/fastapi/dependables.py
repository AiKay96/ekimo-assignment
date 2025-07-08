from typing import Annotated

from fastapi import Depends, Request

from src.infra.repositories.users import UserRepository


def get_user_repository(request: Request) -> UserRepository:
    return request.app.state.users  # type: ignore


UserRepositoryDependable = Annotated[UserRepository, Depends(get_user_repository)]
