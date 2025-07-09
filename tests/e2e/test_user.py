import requests
import pytest

from src.runner.config import settings
from tests.fake import Fake

BASE_URL = settings.base_url


def test_should_create_user() -> None:
    user = Fake().user_dict()
    response = requests.post(f"{BASE_URL}/users", json=user)

    assert response.status_code == 201
    assert response.json() == {"user": user}


def test_should_not_create_duplicate_user() -> None:
    user = Fake().user_dict()

    response = requests.post(f"{BASE_URL}/users", json=user)
    assert response.status_code == 201

    response = requests.post(f"{BASE_URL}/users", json=user)
    assert response.status_code == 409
    assert response.json() == {"message": "User already exists."}
