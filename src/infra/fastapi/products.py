from io import BytesIO
from typing import Any

from fastapi import APIRouter, Depends, UploadFile
from pydantic import BaseModel
from starlette.responses import JSONResponse

from src.core.products import Product
from src.infra.fastapi.dependables import ProductRepositoryDependable, get_current_user
from src.infra.services.product import ProductService

product_api = APIRouter(tags=["Products"])


class SycProductsRequest(BaseModel):
    products: list[Product]


@product_api.put(
    "/products",
    status_code=200,
    response_model=None,
)
def upload_products(
    products: ProductRepositoryDependable,
    file: UploadFile,
    user: str = Depends(get_current_user),  # noqa: ARG001
) -> dict[str, Any] | JSONResponse:
    if (
        file is None
        or file.filename is None
        or not (file.filename.endswith(".csv") or file.filename.endswith(".xlsx"))
    ):
        return JSONResponse(
            status_code=400,
            content={"message": "Only .csv or .xlsx files allowed"},
        )

    service = ProductService(products)
    contents = file.file.read()

    try:
        service.parse_and_update(BytesIO(contents), file.filename)
        return {"message": "Products uploaded successfully"}
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"message": "Failed to process file"},
        )


@product_api.post(
    "/products",
    status_code=201,
    response_model=None,
)
def sync_products(
    repo: ProductRepositoryDependable, products: SycProductsRequest
) -> dict[str, Any] | JSONResponse:
    service = ProductService(repo)

    try:
        service.sync_products(products.products)
        return {"message": "Products synced successfully"}
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"message": "Failed to sync products"},
        )
