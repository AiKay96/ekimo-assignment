import io

import pandas
from fastapi.testclient import TestClient

from tests.fake import Fake


def test_should_upload_products(client: TestClient) -> None:
    user = Fake().user_dict()
    client.post("/users", json=user)

    response = client.post("/auth", data=user)
    token = response.json()["access_token"]

    df = pandas.DataFrame(
        [
            Fake().product_dict(),
            Fake().product_dict(),
        ]
    )
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    response = client.put(
        "/products",
        files={"file": ("products.csv", buffer, "text/csv")},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Products uploaded successfully"}
