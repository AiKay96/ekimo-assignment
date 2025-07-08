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
