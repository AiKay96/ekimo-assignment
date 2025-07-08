from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID, uuid4


@dataclass
class User:
    username: str
    password: str

    id: UUID = field(default_factory=uuid4)


class UserRepository(Protocol):
    def create(self, user: User) -> User:
        pass
