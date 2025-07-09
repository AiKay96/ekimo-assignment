import contextlib

import pytest
import requests
from dotenv import load_dotenv

from src.runner.config import settings

load_dotenv()
BASE_URL = settings.base_url
USERNAME = settings.username
PASSWORD = settings.password


@pytest.fixture(scope="session", autouse=True)
def ensure_user_exists() -> None:
    user = {
        "username": USERNAME,
        "password": PASSWORD,
    }

    with contextlib.suppress(Exception):
        requests.post(f"{BASE_URL}/users", json=user)

    return
