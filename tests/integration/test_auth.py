import io

import pandas
from fastapi.testclient import TestClient

from tests.fake import Fake


def test_should_login(client: TestClient) -> None:
    user = Fake().user_dict()
    client.post("/users", json=user)

    response = client.post("/auth", data=user)

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_should_not_login_on_wrong_password(client: TestClient) -> None:
    user = Fake().user_dict()
    client.post("/users", json=user)

    user["password"] = "wrong_password"
    response = client.post("/auth", data=user)

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_should_not_login_on_unknown_user(client: TestClient) -> None:
    user = Fake().user_dict()

    response = client.post("/auth", data=user)

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_token_structure(client: TestClient) -> None:
    user = Fake().user_dict()
    client.post("/users", json=user)

    response = client.post("/auth", data=user)

    token = response.json()["access_token"]
    parts = token.split(".")
    assert len(parts) == 3


def test_protected_requires_token(client: TestClient) -> None:
    response = client.post("/auth", data=Fake().user_dict())
    assert response.status_code == 401

    df = pandas.DataFrame([Fake().product_dict()])
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    response = client.post(
        "/products",
        files={"file": ("products.csv", buffer, "text/csv")},
    )

    assert response.status_code == 401


def test_should_access_with_token(client: TestClient) -> None:
    user = Fake().user_dict()
    client.post("/users", json=user)

    response = client.post("/auth", data=user)
    token = response.json()["access_token"]

    df = pandas.DataFrame([Fake().product_dict()])
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    response = client.post(
        "/products",
        files={"file": ("products.csv", buffer, "text/csv")},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
