import io

import pandas
import pytest
import requests

from tests.conftest import BASE_URL, PASSWORD, USERNAME
from tests.fake import Fake


@pytest.fixture
def token() -> str:
    response = requests.post(
        f"{BASE_URL}/auth", data={"username": USERNAME, "password": PASSWORD}
    )
    assert response.status_code == 200
    return str(response.json()["access_token"])


def test_should_upload_csv_file(token: str) -> None:
    with open("tests/e2e/test_data/products.csv", "rb") as f:
        files = {"file": ("products.csv", f, "text/csv")}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{BASE_URL}/products", files=files, headers=headers)
    assert response.status_code == 200


def test_should_upload_xlsx_file(token: str) -> None:
    with open("tests/e2e/test_data/products.xlsx", "rb") as f:
        files = {
            "file": (
                "products.xlsx",
                f,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{BASE_URL}/products", files=files, headers=headers)
    assert response.status_code == 200


def test_should_not_upload_invalid_extension(token: str) -> None:
    with open("tests/e2e/test_data/products.txt", "rb") as f:
        files = {"file": ("products.txt", f, "text/plain")}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.put(f"{BASE_URL}/products", files=files, headers=headers)
    assert response.status_code == 400


def test_should_sync_products(token: str) -> None:
    product = Fake().product_dict()

    df = pandas.DataFrame([product])
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    response = requests.put(
        f"{BASE_URL}/products",
        files={"file": ("products.csv", buffer, "text/csv")},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    product["last_updated"] = product["last_updated"].isoformat()
    response = requests.post(
        f"{BASE_URL}/products",
        json={"products": [product]},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
