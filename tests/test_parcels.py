from decimal import Decimal
from unittest.mock import patch

from httpx2 import AsyncClient, ASGITransport

from main import app

import pytest


@pytest.mark.asyncio
async def test_parcel_create_happy_path(client):
    response = await client.post(
        "/api/v1/parcels",
        json={"name": "string", "weight": 1, "type_id": 1, "dollar_price": 1},
    )

    assert response.status_code == 201
    assert response.json()["name"] == "string"
    assert Decimal(response.json()["weight"]) == 1
    assert Decimal(response.json()["dollar_price"]) == 1
    assert response.json()["delivery_price"] == "Не рассчитано"


@pytest.mark.asyncio
async def test_get_user_only_parcels(client):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client2:
        created_parcel_2 = await client2.post(
            "/api/v1/parcels",
            json={"name": "string", "weight": 1, "type_id": 1, "dollar_price": 1},
        )

    created_parcel = await client.post(
        "/api/v1/parcels",
        json={"name": "string", "weight": 1, "type_id": 1, "dollar_price": 1},
    )
    response = await client.get("/api/v1/parcels")
    all_parcels_ids = [parcel["id"] for parcel in response.json()]

    assert created_parcel.json()["id"] in all_parcels_ids
    assert created_parcel_2.json()["id"] not in all_parcels_ids
    assert len(all_parcels_ids) == 1


@pytest.mark.asyncio
async def test_user_get_foreign_parcel(client):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client2:
        created_parcel_2 = await client2.post(
            "/api/v1/parcels",
            json={"name": "string", "weight": 1, "type_id": 1, "dollar_price": 1},
        )
    response = await client.get(f"/api/v1/parcels/{created_parcel_2.json()['id']}")

    assert created_parcel_2.status_code == 201
    assert response.status_code == 404
    assert response.json()["detail"] == "Посылки с таким id не существует"


@pytest.mark.asyncio
async def test_user_get_self_parcel(client):
    response = await client.post(
        "/api/v1/parcels",
        json={"name": "string", "weight": 1, "type_id": 1, "dollar_price": 1},
    )
    assert response.status_code == 201
    parcel_req = await client.get(f"/api/v1/parcels/{response.json()['id']}")

    assert parcel_req.status_code == 200
    assert parcel_req.json()["id"] == response.json()["id"]
    assert parcel_req.json()["name"] == response.json()["name"]
    assert parcel_req.json()["parcel_type"] == response.json()["parcel_type"]
    assert Decimal(parcel_req.json()["weight"]) == Decimal(response.json()["weight"])
    assert parcel_req.json()["delivery_price"] == response.json()["delivery_price"]
    assert Decimal(parcel_req.json()["dollar_price"]) == Decimal(
        response.json()["dollar_price"]
    )


@pytest.mark.asyncio
async def test_create_calculate_delivery_price_task(client):
    with patch("app.api.v1.parcels.calculate_delivery_price_task.delay") as mock_delay:
        mock_delay.return_value.id = "test_mock_id"

        start_calculate = await client.post("api/v1/calculate_delivery_prices")
        assert start_calculate.status_code == 202
        assert start_calculate.json()["task_id"] == "test_mock_id"
        assert start_calculate.json()["status"] == "Added to queue"
        mock_delay.assert_called_once_with()
